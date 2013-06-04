# -*- coding: utf-8 -*-
"""
Pure Python GeoIP API

The API is based on MaxMind's C-based Python API, but the code itself is
ported from the Pure PHP GeoIP API by Jim Winstead and Hans Lellelid.

@author: Jennifer Ennis <zaylea@gmail.com>

@license: Copyright(C) 2004 MaxMind LLC

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.txt>.
"""

import os
import math
import socket
import mmap
import codecs
from threading import Lock

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO

from pygeoip import util, const
from pygeoip.const import PY2, PY3
from pygeoip.timezone import time_zone_by_country_and_region


STANDARD = const.STANDARD
MMAP_CACHE = const.MMAP_CACHE
MEMORY_CACHE = const.MEMORY_CACHE

ENCODING = const.ENCODING


class GeoIPError(Exception):
    pass


class GeoIPMetaclass(type):
    def __new__(cls, *args, **kwargs):
        """
        Singleton method to gets an instance without reparsing the db. Unique
        instances are instantiated based on the filename of the db. Flags are
        ignored for this, i.e. if you initialize one with STANDARD
        flag (default) and then try later to initialize with MEMORY_CACHE, it
        will still return the STANDARD one.
        """
        if not hasattr(cls, '_instances'):
            cls._instances = {}

        if len(args) > 0:
            filename = args[0]
        elif 'filename' in kwargs:
            filename = kwargs['filename']

        if filename not in cls._instances:
            cls._instances[filename] = type.__new__(cls, *args, **kwargs)

        return cls._instances[filename]


GeoIPBase = GeoIPMetaclass('GeoIPBase', (object,), {})


class GeoIP(GeoIPBase):
    def __init__(self, filename, flags=0):
        """
        Initialize the class.

        @param filename: Path to a geoip database.
        @type filename: str
        @param flags: Flags that affect how the database is processed.
            Currently supported flags are STANDARD (the default),
            MEMORY_CACHE (preload the whole file into memory) and
            MMAP_CACHE (access the file via mmap).
        @type flags: int
        """
        self._filename = filename
        self._flags = flags

        if self._flags & const.MMAP_CACHE:
            f = open(filename, 'rb')
            access = mmap.ACCESS_READ
            self._filehandle = mmap.mmap(f.fileno(), 0, access=access)
            f.close()

        elif self._flags & const.MEMORY_CACHE:
            f = open(filename, 'rb')
            self._memoryBuffer = f.read()
            iohandle = BytesIO if PY3 else StringIO
            self._filehandle = iohandle(self._memoryBuffer)
            f.close()

        else:
            self._filehandle = codecs.open(filename, 'rb', ENCODING)

        self._lock = Lock()
        self._setup_segments()

    def _setup_segments(self):
        """
        Parses the database file to determine what kind of database is
        being used and setup segment sizes and start points that will
        be used by the seek*() methods later.

        Supported databases:

        * COUNTRY_EDITION
        * COUNTRY_EDITION_V6
        * REGION_EDITION_REV0
        * REGION_EDITION_REV1
        * CITY_EDITION_REV0
        * CITY_EDITION_REV1
        * CITY_EDITION_REV1_V6
        * ORG_EDITION
        * ISP_EDITION
        * ASNUM_EDITION
        * ASNUM_EDITION_V6

        """
        self._databaseType = const.COUNTRY_EDITION
        self._recordLength = const.STANDARD_RECORD_LENGTH
        self._databaseSegments = const.COUNTRY_BEGIN

        self._lock.acquire()
        filepos = self._filehandle.tell()
        self._filehandle.seek(-3, os.SEEK_END)

        for i in range(const.STRUCTURE_INFO_MAX_SIZE):
            chars = chr(255) * 3
            delim = self._filehandle.read(3)

            if PY3 and type(delim) is bytes:
                delim = delim.decode(ENCODING)

            if PY2:
                chars = chars.decode(ENCODING)
                if type(delim) is str:
                    delim = delim.decode(ENCODING)

            if delim == chars:
                byte = self._filehandle.read(1)
                self._databaseType = ord(byte)

                # Compatibility with databases from April 2003 and earlier
                if (self._databaseType >= 106):
                    self._databaseType -= 105

                if self._databaseType == const.REGION_EDITION_REV0:
                    self._databaseSegments = const.STATE_BEGIN_REV0

                elif self._databaseType == const.REGION_EDITION_REV1:
                    self._databaseSegments = const.STATE_BEGIN_REV1

                elif self._databaseType in (const.CITY_EDITION_REV0,
                                            const.CITY_EDITION_REV1,
                                            const.CITY_EDITION_REV1_V6,
                                            const.ORG_EDITION,
                                            const.ISP_EDITION,
                                            const.ASNUM_EDITION,
                                            const.ASNUM_EDITION_V6):
                    self._databaseSegments = 0
                    buf = self._filehandle.read(const.SEGMENT_RECORD_LENGTH)

                    if PY3 and type(buf) is bytes:
                        buf = buf.decode(ENCODING)

                    for j in range(const.SEGMENT_RECORD_LENGTH):
                        self._databaseSegments += (ord(buf[j]) << (j * 8))

                    LONG_RECORDS = (const.ORG_EDITION, const.ISP_EDITION)
                    if self._databaseType in LONG_RECORDS:
                        self._recordLength = const.ORG_RECORD_LENGTH
                break
            else:
                self._filehandle.seek(-4, os.SEEK_CUR)

        self._filehandle.seek(filepos, os.SEEK_SET)
        self._lock.release()

    def _seek_country(self, ipnum):
        """
        Using the record length and appropriate start points, seek to the
        country that corresponds to the converted IP address integer.

        @param ipnum: result of ip2long conversion
        @type ipnum: int
        @return: offset of start of record
        @rtype: int
        """
        try:
            offset = 0
            seek_depth = 127 if len(str(ipnum)) > 10 else 31

            for depth in range(seek_depth, -1, -1):
                if self._flags & const.MEMORY_CACHE:
                    startIndex = 2 * self._recordLength * offset
                    endIndex = startIndex + (2 * self._recordLength)
                    buf = self._memoryBuffer[startIndex:endIndex]
                else:
                    startIndex = 2 * self._recordLength * offset
                    readLength = 2 * self._recordLength
                    self._lock.acquire()
                    self._filehandle.seek(startIndex, os.SEEK_SET)
                    buf = self._filehandle.read(readLength)
                    self._lock.release()

                if PY3 and type(buf) is bytes:
                    buf = buf.decode(ENCODING)

                x = [0, 0]
                for i in range(2):
                    for j in range(self._recordLength):
                        byte = buf[self._recordLength * i + j]
                        x[i] += ord(byte) << (j * 8)
                if ipnum & (1 << depth):
                    if x[1] >= self._databaseSegments:
                        return x[1]
                    offset = x[1]
                else:
                    if x[0] >= self._databaseSegments:
                        return x[0]
                    offset = x[0]
        except:
            pass

        raise GeoIPError('Corrupt database')

    def _get_org(self, ipnum):
        """
        Seek and return organization or ISP name for ipnum.
        @param ipnum: Converted IP address
        @type ipnum: int
        @return: org/isp name
        @rtype: str
        """
        seek_org = self._seek_country(ipnum)
        if seek_org == self._databaseSegments:
            return None

        read_length = (2 * self._recordLength - 1) * self._databaseSegments
        self._lock.acquire()
        self._filehandle.seek(seek_org + read_length, os.SEEK_SET)
        buf = self._filehandle.read(const.MAX_ORG_RECORD_LENGTH)
        self._lock.release()

        if PY3 and type(buf) is bytes:
            buf = buf.decode(ENCODING)

        return buf[:buf.index(chr(0))]

    def _get_region(self, ipnum):
        """
        Seek and return the region info (dict containing country_code
        and region_name).

        @param ipnum: Converted IP address
        @type ipnum: int
        @return: dict containing country_code and region_name
        @rtype: dict
        """
        region = ''
        country_code = ''
        seek_country = self._seek_country(ipnum)

        def get_region_name(offset):
            region1 = chr(offset // 26 + 65)
            region2 = chr(offset % 26 + 65)
            return ''.join([region1, region2])

        if self._databaseType == const.REGION_EDITION_REV0:
            seek_region = seek_country - const.STATE_BEGIN_REV0
            if seek_region >= 1000:
                country_code = 'US'
                region = get_region_name(seek_region - 1000)
            else:
                country_code = const.COUNTRY_CODES[seek_region]
        elif self._databaseType == const.REGION_EDITION_REV1:
            seek_region = seek_country - const.STATE_BEGIN_REV1
            if seek_region < const.US_OFFSET:
                pass
            elif seek_region < const.CANADA_OFFSET:
                country_code = 'US'
                region = get_region_name(seek_region - const.US_OFFSET)
            elif seek_region < const.WORLD_OFFSET:
                country_code = 'CA'
                region = get_region_name(seek_region - const.CANADA_OFFSET)
            else:
                index = (seek_region - const.WORLD_OFFSET) // const.FIPS_RANGE
                if index in const.COUNTRY_CODES:
                    country_code = const.COUNTRY_CODES[index]
        elif self._databaseType in const.CITY_EDITIONS:
            rec = self._get_record(ipnum)
            region = rec.get('region_name', '')
            country_code = rec.get('country_code', '')

        return {'country_code': country_code, 'region_name': region}

    def _get_record(self, ipnum):
        """
        Populate location dict for converted IP.

        @param ipnum: Converted IP address
        @type ipnum: int
        @return: dict with country_code, country_code3, country_name,
            region, city, postal_code, latitude, longitude,
            dma_code, metro_code, area_code, region_name, time_zone
        @rtype: dict
        """
        seek_country = self._seek_country(ipnum)
        if seek_country == self._databaseSegments:
            return {}

        read_length = (2 * self._recordLength - 1) * self._databaseSegments
        self._lock.acquire()
        self._filehandle.seek(seek_country + read_length, os.SEEK_SET)
        buf = self._filehandle.read(const.FULL_RECORD_LENGTH)
        self._lock.release()

        if PY3 and type(buf) is bytes:
            buf = buf.decode(ENCODING)

        record = {
            'dma_code': 0,
            'area_code': 0,
            'metro_code': '',
            'postal_code': ''
        }

        latitude = 0
        longitude = 0
        buf_pos = 0

        # Get country
        char = ord(buf[buf_pos])
        record['country_code'] = const.COUNTRY_CODES[char]
        record['country_code3'] = const.COUNTRY_CODES3[char]
        record['country_name'] = const.COUNTRY_NAMES[char]
        record['continent'] = const.CONTINENT_NAMES[char]

        buf_pos += 1
        def get_data(buf, buf_pos):
            offset = buf_pos
            char = ord(buf[offset])
            while (char != 0):
                offset += 1
                char = ord(buf[offset])
            if offset > buf_pos:
                return (offset, buf[buf_pos:offset])
            return (offset, '')

        offset, record['region_name'] = get_data(buf, buf_pos)
        offset, record['city'] = get_data(buf, offset + 1)
        offset, record['postal_code'] = get_data(buf, offset + 1)
        buf_pos = offset + 1

        for j in range(3):
            char = ord(buf[buf_pos])
            buf_pos += 1
            latitude += (char << (j * 8))

        for j in range(3):
            char = ord(buf[buf_pos])
            buf_pos += 1
            longitude += (char << (j * 8))

        record['latitude'] = (latitude / 10000.0) - 180.0
        record['longitude'] = (longitude / 10000.0) - 180.0

        if self._databaseType in (const.CITY_EDITION_REV1, const.CITY_EDITION_REV1_V6):
            dmaarea_combo = 0
            if record['country_code'] == 'US':
                for j in range(3):
                    char = ord(buf[buf_pos])
                    dmaarea_combo += (char << (j * 8))
                    buf_pos += 1

                record['dma_code'] = int(math.floor(dmaarea_combo / 1000))
                record['area_code'] = dmaarea_combo % 1000

        record['metro_code'] = const.DMA_MAP.get(record['dma_code'])
        params = (record['country_code'], record['region_name'])
        record['time_zone'] = time_zone_by_country_and_region(*params)

        return record

    def _gethostbyname(self, hostname):
        if self._databaseType in const.IPV6_EDITIONS:
            try:
                response = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
                family, socktype, proto, canonname, sockaddr = response[0]
                address, port, flow, scope = sockaddr
                return address
            except socket.gaierror:
                return ''
        else:
            return socket.gethostbyname(hostname)

    def id_by_addr(self, addr):
        """
        Get the country index.
        Looks up the index for the country which is the key for
        the code and name.

        @param addr: The IP address
        @type addr: str
        @return: network byte order 32-bit integer
        @rtype: int
        """
        ipnum = util.ip2long(addr)
        if not ipnum:
            raise ValueError("Invalid IP address: %s" % addr)

        COUNTY_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
        if self._databaseType not in COUNTY_EDITIONS:
            message = 'Invalid database type, expected Country'
            raise GeoIPError(message)

        return self._seek_country(ipnum) - const.COUNTRY_BEGIN

    def country_code_by_addr(self, addr):
        """
        Returns 2-letter country code (e.g. 'US') for specified IP address.
        Use this method if you have a Country, Region, or City database.

        @param addr: IP address
        @type addr: str
        @return: 2-letter country code
        @rtype: str
        """
        try:
            VALID_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
            if self._databaseType in VALID_EDITIONS:
                ipv = 6 if addr.find(':') >= 0 else 4

                if ipv == 4 and self._databaseType != const.COUNTRY_EDITION:
                    message = 'Invalid database type; expected IPv6 address'
                    raise ValueError(message)
                if ipv == 6 and self._databaseType != const.COUNTRY_EDITION_V6:
                    message = 'Invalid database type; expected IPv4 address'
                    raise ValueError(message)

                country_id = self.id_by_addr(addr)
                return const.COUNTRY_CODES[country_id]
            elif self._databaseType in const.REGION_CITY_EDITIONS:
                return self.region_by_addr(addr).get('country_code')

            message = 'Invalid database type, expected Country, City or Region'
            raise GeoIPError(message)
        except ValueError:
            raise GeoIPError('Failed to lookup address %s' % addr)

    def country_code_by_name(self, hostname):
        """
        Returns 2-letter country code (e.g. 'US') for specified hostname.
        Use this method if you have a Country, Region, or City database.

        @param hostname: Hostname
        @type hostname: str
        @return: 2-letter country code
        @rtype: str
        """
        addr = self._gethostbyname(hostname)
        return self.country_code_by_addr(addr)

    def country_name_by_addr(self, addr):
        """
        Returns full country name for specified IP address.
        Use this method if you have a Country or City database.

        @param addr: IP address
        @type addr: str
        @return: country name
        @rtype: str
        """
        try:
            VALID_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
            if self._databaseType in VALID_EDITIONS:
                country_id = self.id_by_addr(addr)
                return const.COUNTRY_NAMES[country_id]
            elif self._databaseType in const.CITY_EDITIONS:
                return self.record_by_addr(addr).get('country_name')
            else:
                message = 'Invalid database type, expected Country or City'
                raise GeoIPError(message)
        except ValueError:
            raise GeoIPError('Failed to lookup address %s' % addr)

    def country_name_by_name(self, hostname):
        """
        Returns full country name for specified hostname.
        Use this method if you have a Country database.

        @param hostname: Hostname
        @type hostname: str
        @return: country name
        @rtype: str
        """
        addr = self._gethostbyname(hostname)
        return self.country_name_by_addr(addr)

    def org_by_addr(self, addr):
        """
        Lookup Organization, ISP or ASNum for given IP address.
        Use this method if you have an Organization, ISP or ASNum database.

        @param addr: IP address
        @type addr: str
        @return: organization or ISP name
        @rtype: str
        """
        try:
            ipnum = util.ip2long(addr)
            if not ipnum:
                raise ValueError('Invalid IP address')

            valid = (const.ORG_EDITION, const.ISP_EDITION, const.ASNUM_EDITION, const.ASNUM_EDITION_V6)
            if self._databaseType not in valid:
                message = 'Invalid database type, expected Org, ISP or ASNum'
                raise GeoIPError(message)

            return self._get_org(ipnum)
        except ValueError:
            raise GeoIPError('Failed to lookup address %s' % addr)

    def org_by_name(self, hostname):
        """
        Lookup the organization (or ISP) for hostname.
        Use this method if you have an Organization/ISP database.

        @param hostname: Hostname
        @type hostname: str
        @return: Organization or ISP name
        @rtype: str
        """
        addr = self._gethostbyname(hostname)
        return self.org_by_addr(addr)

    def record_by_addr(self, addr):
        """
        Look up the record for a given IP address.
        Use this method if you have a City database.

        @param addr: IP address
        @type addr: str
        @return: Dictionary with country_code, country_code3, country_name,
            region, city, postal_code, latitude, longitude, dma_code,
            metro_code, area_code, region_name, time_zone
        @rtype: dict
        """
        try:
            ipnum = util.ip2long(addr)
            if not ipnum:
                raise ValueError('Invalid IP address')

            if self._databaseType not in const.CITY_EDITIONS:
                message = 'Invalid database type, expected City'
                raise GeoIPError(message)

            rec = self._get_record(ipnum)
            if not rec:
                return None

            return rec
        except ValueError:
            raise GeoIPError('Failed to lookup address %s' % addr)

    def record_by_name(self, hostname):
        """
        Look up the record for a given hostname.
        Use this method if you have a City database.

        @param hostname: Hostname
        @type hostname: str
        @return: Dictionary with country_code, country_code3, country_name,
            region, city, postal_code, latitude, longitude, dma_code,
            metro_code, area_code, region_name, time_zone
        @rtype: dict
        """
        addr = self._gethostbyname(hostname)
        return self.record_by_addr(addr)

    def region_by_addr(self, addr):
        """
        Lookup the region for given IP address.
        Use this method if you have a Region database.

        @param addr: IP address
        @type addr: str
        @return: Dictionary containing country_code, region and region_name
        @rtype: dict
        """
        try:
            ipnum = util.ip2long(addr)
            if not ipnum:
                raise ValueError('Invalid IP address')

            if self._databaseType not in const.REGION_CITY_EDITIONS:
                message = 'Invalid database type, expected Region or City'
                raise GeoIPError(message)

            return self._get_region(ipnum)
        except ValueError:
            raise GeoIPError('Failed to lookup address %s' % addr)

    def region_by_name(self, hostname):
        """
        Lookup the region for given hostname.
        Use this method if you have a Region database.

        @param hostname: Hostname
        @type hostname: str
        @return: Dictionary containing country_code, region, and region_name
        @rtype: dict
        """
        addr = self._gethostbyname(hostname)
        return self.region_by_addr(addr)

    def time_zone_by_addr(self, addr):
        """
        Look up the time zone for a given IP address.
        Use this method if you have a Region or City database.

        @param addr: IP address
        @type addr: str
        @return: Time zone
        @rtype: str
        """
        try:
            ipnum = util.ip2long(addr)
            if not ipnum:
                raise ValueError('Invalid IP address')

            if self._databaseType not in const.CITY_EDITIONS:
                message = 'Invalid database type, expected City'
                raise GeoIPError(message)

            return self._get_record(ipnum).get('time_zone')
        except ValueError:
            raise GeoIPError('Failed to lookup address %s' % addr)

    def time_zone_by_name(self, hostname):
        """
        Look up the time zone for a given hostname.
        Use this method if you have a Region or City database.

        @param hostname: Hostname
        @type hostname: str
        @return: Time zone
        @rtype: str
        """
        addr = self._gethostbyname(hostname)
        return self.time_zone_by_addr(addr)
