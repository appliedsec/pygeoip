# -*- coding: utf-8 -*-
"""
Copyright (c) 2010-2014 Jennifer Ennis, William Tisäter.

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

__version__ = "0.3.2"

import os
import socket
import codecs
from math import floor
from threading import Lock

try:
    import mmap
except ImportError:  # pragma: no cover
    mmap = None

from pygeoip import util, const
from pygeoip.const import PY2, PY3
from pygeoip.timezone import time_zone_by_country_and_region

range = xrange if PY2 else range

STANDARD = const.STANDARD
MMAP_CACHE = const.MMAP_CACHE
MEMORY_CACHE = const.MEMORY_CACHE

ENCODING = const.ENCODING


class GeoIPError(Exception):
    """
    Thin wrapper of `Exception`, will be thrown in case of an
    unrecoverable error.
    """
    pass


class _GeoIPMetaclass(type):
    _instances = {}
    _instance_lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Singleton method to gets an instance without reparsing
        the database, the filename is being used as cache key.
        """
        if len(args) > 0:
            filename = args[0]
        elif 'filename' in kwargs:
            filename = kwargs['filename']
        else:
            return None

        if not kwargs.get('cache', True):
            return super(_GeoIPMetaclass, cls).__call__(*args, **kwargs)

        try:
            cls._instance_lock.acquire()
            if filename not in cls._instances:
                cls._instances[filename] = super(_GeoIPMetaclass, cls).__call__(*args, **kwargs)
        finally:
            cls._instance_lock.release()

        return cls._instances[filename]


class GeoIP(object):
    __metaclass__ = _GeoIPMetaclass

    def __init__(self, filename, flags=STANDARD, cache=True):
        """
        Create and return an GeoIP instance.

        :arg filename: File path to a GeoIP database
        :arg flags: Flags that affect how the database is processed.
            Currently supported flags are STANDARD (default),
            MEMORY_CACHE (preload the whole file into memory) and
            MMAP_CACHE (access the file via mmap)
        :arg cache: Used in tests to skip instance caching
        """
        self._lock = Lock()
        self._flags = flags
        self._netmask = None

        if self._flags & const.MMAP_CACHE and mmap is None:  # pragma: no cover
            import warnings
            warnings.warn("MMAP_CACHE cannot be used without a mmap module")
            self._flags &= ~const.MMAP_CACHE

        if self._flags & const.MMAP_CACHE:
            f = codecs.open(filename, 'rb', ENCODING)
            access = mmap.ACCESS_READ
            self._fp = mmap.mmap(f.fileno(), 0, access=access)
            self._type = 'MMAP_CACHE'
            f.close()
        elif self._flags & const.MEMORY_CACHE:
            f = codecs.open(filename, 'rb', ENCODING)
            self._memory = f.read()
            self._fp = util.str2fp(self._memory)
            self._type = 'MEMORY_CACHE'
            f.close()
        else:
            self._fp = codecs.open(filename, 'rb', ENCODING)
            self._type = 'STANDARD'

        try:
            self._lock.acquire()
            self._setup_segments()
        finally:
            self._lock.release()

    def _setup_segments(self):
        """
        Parses the database file to determine what kind of database is
        being used and setup segment sizes and start points that will
        be used by the seek*() methods later.
        """
        self._databaseType = const.COUNTRY_EDITION
        self._recordLength = const.STANDARD_RECORD_LENGTH
        self._databaseSegments = const.COUNTRY_BEGIN

        filepos = self._fp.tell()
        self._fp.seek(-3, os.SEEK_END)

        for i in range(const.STRUCTURE_INFO_MAX_SIZE):
            chars = chr(255) * 3
            delim = self._fp.read(3)

            if PY3 and type(delim) is bytes:
                delim = delim.decode(ENCODING)

            if PY2:
                chars = chars.decode(ENCODING)
                if type(delim) is str:
                    delim = delim.decode(ENCODING)

            if delim == chars:
                byte = self._fp.read(1)
                self._databaseType = ord(byte)

                # Compatibility with databases from April 2003 and earlier
                if self._databaseType >= 106:
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
                                            const.NETSPEED_EDITION_REV1,
                                            const.NETSPEED_EDITION_REV1_V6,
                                            const.ASNUM_EDITION,
                                            const.ASNUM_EDITION_V6):
                    self._databaseSegments = 0
                    buf = self._fp.read(const.SEGMENT_RECORD_LENGTH)

                    if PY3 and type(buf) is bytes:
                        buf = buf.decode(ENCODING)

                    for j in range(const.SEGMENT_RECORD_LENGTH):
                        self._databaseSegments += (ord(buf[j]) << (j * 8))

                    LONG_RECORDS = (const.ORG_EDITION, const.ISP_EDITION)
                    if self._databaseType in LONG_RECORDS:
                        self._recordLength = const.ORG_RECORD_LENGTH
                break
            else:
                self._fp.seek(-4, os.SEEK_CUR)

        self._fp.seek(filepos, os.SEEK_SET)

    def _seek_country(self, ipnum):
        """
        Using the record length and appropriate start points, seek to the
        country that corresponds to the converted IP address integer.
        Return offset of record.

        :arg ipnum: Result of ip2long conversion
        """
        try:
            offset = 0
            seek_depth = 127 if len(str(ipnum)) > 10 else 31

            for depth in range(seek_depth, -1, -1):
                if self._flags & const.MEMORY_CACHE:
                    startIndex = 2 * self._recordLength * offset
                    endIndex = startIndex + (2 * self._recordLength)
                    buf = self._memory[startIndex:endIndex]
                else:
                    startIndex = 2 * self._recordLength * offset
                    readLength = 2 * self._recordLength
                    try:
                        self._lock.acquire()
                        self._fp.seek(startIndex, os.SEEK_SET)
                        buf = self._fp.read(readLength)
                    finally:
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
                        self._netmask = seek_depth - depth + 1
                        return x[1]
                    offset = x[1]
                else:
                    if x[0] >= self._databaseSegments:
                        self._netmask = seek_depth - depth + 1
                        return x[0]
                    offset = x[0]
        except (IndexError, UnicodeDecodeError):
            pass

        raise GeoIPError('Corrupt database')

    def _get_org(self, ipnum):
        """
        Seek and return organization or ISP name for ipnum.
        Return org/isp name.

        :arg ipnum: Result of ip2long conversion
        """
        seek_org = self._seek_country(ipnum)
        if seek_org == self._databaseSegments:
            return None

        read_length = (2 * self._recordLength - 1) * self._databaseSegments
        try:
            self._lock.acquire()
            self._fp.seek(seek_org + read_length, os.SEEK_SET)
            buf = self._fp.read(const.MAX_ORG_RECORD_LENGTH)
        finally:
            self._lock.release()

        if PY3 and type(buf) is bytes:
            buf = buf.decode(ENCODING)

        return buf[:buf.index(chr(0))]

    def _get_region(self, ipnum):
        """
        Seek and return the region information.
        Returns dict containing country_code and region_code.

        :arg ipnum: Result of ip2long conversion
        """
        region_code = None
        country_code = None
        seek_country = self._seek_country(ipnum)

        def get_region_code(offset):
            region1 = chr(offset // 26 + 65)
            region2 = chr(offset % 26 + 65)
            return ''.join([region1, region2])

        if self._databaseType == const.REGION_EDITION_REV0:
            seek_region = seek_country - const.STATE_BEGIN_REV0
            if seek_region >= 1000:
                country_code = 'US'
                region_code = get_region_code(seek_region - 1000)
            else:
                country_code = const.COUNTRY_CODES[seek_region]
        elif self._databaseType == const.REGION_EDITION_REV1:
            seek_region = seek_country - const.STATE_BEGIN_REV1
            if seek_region < const.US_OFFSET:
                pass
            elif seek_region < const.CANADA_OFFSET:
                country_code = 'US'
                region_code = get_region_code(seek_region - const.US_OFFSET)
            elif seek_region < const.WORLD_OFFSET:
                country_code = 'CA'
                region_code = get_region_code(seek_region - const.CANADA_OFFSET)
            else:
                index = (seek_region - const.WORLD_OFFSET) // const.FIPS_RANGE
                if index < len(const.COUNTRY_CODES):
                    country_code = const.COUNTRY_CODES[index]
        elif self._databaseType in const.CITY_EDITIONS:
            rec = self._get_record(ipnum)
            region_code = rec.get('region_code')
            country_code = rec.get('country_code')

        return {'country_code': country_code, 'region_code': region_code}

    def _get_record(self, ipnum):
        """
        Populate location dict for converted IP.
        Returns dict with numerous location properties.

        :arg ipnum: Result of ip2long conversion
        """
        seek_country = self._seek_country(ipnum)
        if seek_country == self._databaseSegments:
            return {}

        read_length = (2 * self._recordLength - 1) * self._databaseSegments
        try:
            self._lock.acquire()
            self._fp.seek(seek_country + read_length, os.SEEK_SET)
            buf = self._fp.read(const.FULL_RECORD_LENGTH)
        finally:
            self._lock.release()

        if PY3 and type(buf) is bytes:
            buf = buf.decode(ENCODING)

        record = {
            'dma_code': 0,
            'area_code': 0,
            'metro_code': None,
            'postal_code': None
        }

        latitude = 0
        longitude = 0

        char = ord(buf[0])
        record['country_code'] = const.COUNTRY_CODES[char]
        record['country_code3'] = const.COUNTRY_CODES3[char]
        record['country_name'] = const.COUNTRY_NAMES[char]
        record['continent'] = const.CONTINENT_NAMES[char]

        def read_data(buf, pos):
            cur = pos
            while buf[cur] != '\0':
                cur += 1
            return cur, buf[pos:cur] if cur > pos else None

        offset, record['region_code'] = read_data(buf, 1)
        offset, record['city'] = read_data(buf, offset + 1)
        offset, record['postal_code'] = read_data(buf, offset + 1)
        offset = offset + 1

        for j in range(3):
            latitude += (ord(buf[offset + j]) << (j * 8))

        for j in range(3):
            longitude += (ord(buf[offset + j + 3]) << (j * 8))

        record['latitude'] = (latitude / 10000.0) - 180.0
        record['longitude'] = (longitude / 10000.0) - 180.0

        if self._databaseType in (const.CITY_EDITION_REV1, const.CITY_EDITION_REV1_V6):
            if record['country_code'] == 'US':
                dma_area = 0
                for j in range(3):
                    dma_area += ord(buf[offset + j + 6]) << (j * 8)

                record['dma_code'] = int(floor(dma_area / 1000))
                record['area_code'] = dma_area % 1000
                record['metro_code'] = const.DMA_MAP.get(record['dma_code'])

        params = (record['country_code'], record['region_code'])
        record['time_zone'] = time_zone_by_country_and_region(*params)

        return record

    def _gethostbyname(self, hostname):
        """
        Hostname lookup method, supports both IPv4 and IPv6.
        """
        if self._databaseType in const.IPV6_EDITIONS:
            response = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
            family, socktype, proto, canonname, sockaddr = response[0]
            address, port, flow, scope = sockaddr
            return address
        else:
            return socket.gethostbyname(hostname)

    def id_by_name(self, hostname):
        """
        Returns the database ID for specified hostname.
        The id might be useful as array index. 0 is unknown.

        :arg hostname: Hostname to get ID from.
        """
        addr = self._gethostbyname(hostname)
        return self.id_by_addr(addr)

    def id_by_addr(self, addr):
        """
        Returns the database ID for specified address.
        The ID might be useful as array index. 0 is unknown.

        :arg addr: IPv4 or IPv6 address (eg. 203.0.113.30)
        """
        if self._databaseType in (const.PROXY_EDITION, const.NETSPEED_EDITION_REV1, const.NETSPEED_EDITION_REV1_V6):
            raise GeoIPError('Invalid database type; this database is not supported')
        ipv = 6 if addr.find(':') >= 0 else 4
        if ipv == 4 and self._databaseType not in (const.COUNTRY_EDITION, const.NETSPEED_EDITION):
            raise GeoIPError('Invalid database type; this database supports IPv6 addresses, not IPv4')
        if ipv == 6 and self._databaseType != const.COUNTRY_EDITION_V6:
            raise GeoIPError('Invalid database type; this database supports IPv4 addresses, not IPv6')

        ipnum = util.ip2long(addr)
        return self._seek_country(ipnum) - const.COUNTRY_BEGIN

    def last_netmask(self):
        """
        Returns the netmask depth of the last lookup.
        """
        return self._netmask

    def country_code_by_addr(self, addr):
        """
        Returns 2-letter country code (e.g. US) from IP address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        VALID_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
        if self._databaseType in VALID_EDITIONS:
            country_id = self.id_by_addr(addr)
            return const.COUNTRY_CODES[country_id]
        elif self._databaseType in const.REGION_CITY_EDITIONS:
            return self.region_by_addr(addr).get('country_code')

        raise GeoIPError('Invalid database type, expected Country, City or Region')

    def country_code_by_name(self, hostname):
        """
        Returns 2-letter country code (e.g. US) from hostname.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.country_code_by_addr(addr)

    def netspeed_by_addr(self, addr):
        """
        Returns NetSpeed name from address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType == const.NETSPEED_EDITION:
            return const.NETSPEED_NAMES[self.id_by_addr(addr)]
        elif self._databaseType in (const.NETSPEED_EDITION_REV1,
                                    const.NETSPEED_EDITION_REV1_V6):
            ipnum = util.ip2long(addr)
            return self._get_org(ipnum)

        raise GeoIPError(
            'Invalid database type, expected NetSpeed or NetSpeedCell')

    def netspeed_by_name(self, hostname):
        """
        Returns NetSpeed name from hostname. Can be Unknown, Dial-up,
        Cable, or Corporate.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.netspeed_by_addr(addr)

    def country_name_by_addr(self, addr):
        """
        Returns full country name for specified IP address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        VALID_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
        if self._databaseType in VALID_EDITIONS:
            country_id = self.id_by_addr(addr)
            return const.COUNTRY_NAMES[country_id]
        elif self._databaseType in const.CITY_EDITIONS:
            return self.record_by_addr(addr).get('country_name')
        else:
            message = 'Invalid database type, expected Country or City'
            raise GeoIPError(message)

    def country_name_by_name(self, hostname):
        """
        Returns full country name for specified hostname.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.country_name_by_addr(addr)

    def org_by_addr(self, addr):
        """
        Returns Organization, ISP, or ASNum name for given IP address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        valid = (const.ORG_EDITION, const.ISP_EDITION,
                 const.ASNUM_EDITION, const.ASNUM_EDITION_V6)
        if self._databaseType not in valid:
            message = 'Invalid database type, expected Org, ISP or ASNum'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        return self._get_org(ipnum)

    def org_by_name(self, hostname):
        """
        Returns Organization, ISP, or ASNum name for given hostname.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.org_by_addr(addr)

    isp_by_addr = org_by_addr
    isp_by_name = org_by_name
    asn_by_addr = org_by_addr
    asn_by_name = org_by_name

    def record_by_addr(self, addr):
        """
        Returns dictionary with city data containing `country_code`, `country_name`,
        `region`, `city`, `postal_code`, `latitude`, `longitude`, `dma_code`,
        `metro_code`, `area_code`, `region_code` and `time_zone`.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType not in const.CITY_EDITIONS:
            message = 'Invalid database type, expected City'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        rec = self._get_record(ipnum)
        if not rec:
            return None

        return rec

    def record_by_name(self, hostname):
        """
        Returns dictionary with city data containing `country_code`, `country_name`,
        `region`, `city`, `postal_code`, `latitude`, `longitude`, `dma_code`,
        `metro_code`, `area_code`, `region_code` and `time_zone`.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.record_by_addr(addr)

    def region_by_addr(self, addr):
        """
        Returns dictionary containing `country_code` and `region_code`.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType not in const.REGION_CITY_EDITIONS:
            message = 'Invalid database type, expected Region or City'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        return self._get_region(ipnum)

    def region_by_name(self, hostname):
        """
        Returns dictionary containing `country_code` and `region_code`.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.region_by_addr(addr)

    def time_zone_by_addr(self, addr):
        """
        Returns time zone in tzdata format (e.g. America/New_York or Europe/Paris)

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType not in const.CITY_EDITIONS:
            message = 'Invalid database type, expected City'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        return self._get_record(ipnum).get('time_zone')

    def time_zone_by_name(self, hostname):
        """
        Returns time zone in tzdata format (e.g. America/New_York or Europe/Paris)

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.time_zone_by_addr(addr)
