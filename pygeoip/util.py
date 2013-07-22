# -*- coding: utf-8 -*-
"""
Utility function for address translation

@author: Jennifer Ennis <zaylea@gmail.com>
@author: William Tisäter <william@defunct.cc>

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

import socket
import binascii


def ip2long(ip):
    """
    Wrapper function for IPv4 and IPv6 converters
    @param ip: IPv4 or IPv6 address
    @type ip: str
    """
    try:
        return int(binascii.hexlify(socket.inet_aton(ip)), 16)
    except socket.error:
        return int(binascii.hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)
