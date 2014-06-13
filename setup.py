#!/usr/bin/env python
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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pygeoip import __version__

setup(name='pygeoip',
      version=__version__,
      description='Pure Python GeoIP API',
      author='Jennifer Ennis',
      author_email='zaylea@gmail.com',
      maintainer='William Tisäter',
      maintainer_email='william@defunct.cc',
      url='https://github.com/appliedsec/pygeoip',
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4'],
      packages=['pygeoip'],
      license='LGPLv3+',
      keywords='geoip')
