# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

import pygeoip
from tests.config import ASNUM_DB_PATH


class TestGeoIPASNumFunctions(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(ASNUM_DB_PATH)

    def testOrgByAddr(self):
        asn = self.gi.asn_by_addr('64.17.254.216')
        self.assertEqual(asn, 'AS33224')

    @raises(pygeoip.GeoIPError)
    def testCodeByAddr(self):
        self.gi.country_code_by_addr('64.17.254.216')

    @raises(pygeoip.GeoIPError)
    def testNameByAddr(self):
        self.gi.country_name_by_addr('64.17.254.216')
