# -*- coding: utf-8 -*-
import socket
import unittest
from nose.tools import raises

import pygeoip
from pygeoip import const
from tests.config import COUNTRY_DB_PATH, CORRUPT_DB_PATH

class TestGenerals(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(filename=COUNTRY_DB_PATH)
        self.assertEqual(self.gi._type, 'STANDARD')

    def testConstLengths(self):
        assert len(const.COUNTRY_CODES) == len(const.COUNTRY_CODES3)
        assert len(const.COUNTRY_CODES) == len(const.COUNTRY_NAMES)
        assert len(const.COUNTRY_CODES) == len(const.CONTINENT_NAMES)

    @raises(pygeoip.GeoIPError)
    def testCorruptDatabase(self):
        gi = pygeoip.GeoIP(filename=CORRUPT_DB_PATH)
        gi.country_code_by_name('google.com')

    @raises(socket.error)
    def testInvalidAddress(self):
        self.gi.country_code_by_addr('google.com')

    def testGetEmptyRecord(self):
        self.gi._get_record(0)
