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
    
    return int(socket.inet_aton(ip).encode('hex'), 16)




def ip2long_v6(ip):
    """
    Convert a IPv6 address into long.

    @param ip: IPv6 address
    @type ip: str
    @return: network byte order long
    @rtype: long
    """
    return int(socket.inet_pton(socket.AF_INET6, ip).encode('hex'), 16)
