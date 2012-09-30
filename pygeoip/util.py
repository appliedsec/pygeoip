# -*- coding: utf-8 -*-
"""
Utility functions. Part of the pygeoip package.

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

import struct
import socket
from array import array

from pygeoip.const import PY3


def ip2long(ip):
    """
    Wrapper function for IPv4 and IPv6 converters
    @param ip: IPv4 or IPv6 address
    @type ip: str
    """
    if ip.find(':') >= 0:
        return ip2long_v6(ip)
    else:
        return ip2long_v4(ip)


def ip2long_v4(ip):
    """
    Convert a IPv4 address into a 32-bit integer.

    @param ip: quad-dotted IPv4 address
    @type ip: str
    @return: network byte order 32-bit integer
    @rtype: int
    """
    ip_array = ip.split('.')
    if PY3:
        # int and long are unified in py3
        return int(ip_array[0]) * 16777216 + int(ip_array[1]) * 65536 + \
            int(ip_array[2]) * 256 + int(ip_array[3])
    else:
        return long(ip_array[0]) * 16777216 + long(ip_array[1]) * 65536 + \
            long(ip_array[2]) * 256 + long(ip_array[3])


def ip2long_v6(ip):
    """
    Convert a IPv6 address into long.

    @param ip: IPv6 address
    @type ip: str
    @return: network byte order long
    @rtype: long
    """
    ipbyte = socket.inet_pton(socket.AF_INET6, ip)
    ipnum = array('L', struct.unpack('!4L', ipbyte))
    max_index = len(ipnum) - 1
    return sum(ipnum[max_index - i] << (i * 32) for i in range(len(ipnum)))
