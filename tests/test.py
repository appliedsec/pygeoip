# -*- coding: utf-8 -*-
import socket
import unittest
from nose.tools import raises

import pygeoip
from pygeoip import const
from tests.config import COUNTRY_DB_PATH

class TestGenerals(unittest.TestCase):
    def testContructing(self):
        gi = pygeoip.GeoIP(filename=COUNTRY_DB_PATH)
        self.assertEqual(gi._type, 'STANDARD')

    def testConstLengths(self):
        assert len(const.COUNTRY_CODES) == len(const.COUNTRY_CODES3)
        assert len(const.COUNTRY_CODES) == len(const.COUNTRY_NAMES)
        assert len(const.COUNTRY_CODES) == len(const.CONTINENT_NAMES)

    @raises(socket.gaierror)
    def testFailedLookup(self):
        gi = pygeoip.GeoIP(filename=COUNTRY_DB_PATH)
        gi.country_code_by_name('google')

    @raises(socket.error)
    def testInvalidAddress(self):
        gi = pygeoip.GeoIP(filename=COUNTRY_DB_PATH)
        gi.country_code_by_addr('google.com')
