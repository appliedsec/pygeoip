#!/usr/bin/env python

"""
Setup file for pygeoip package.

@author: Jennifer Ennis <zaylea at gmail dot com>

@license:
Copyright(C) 2004 MaxMind LLC

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


setup(name='pygeoip',
      version='0.2.5',
      description='Pure Python GeoIP API',
      author='Jennifer Ennis',
      author_email='zaylea@gmail.com',
      url='http://code.google.com/p/pygeoip/',
      classifiers=['License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2'],
      packages=['pygeoip'],
      install_requires=['six'],
      license='LGPLv3+',
      keywords='geoip')
