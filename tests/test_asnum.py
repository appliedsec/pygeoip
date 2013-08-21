# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

import pygeoip
from tests.config import ASNUM_DB_PATH


class TestGeoIPASNumFunctions(unittest.TestCase):
    def setUp(self):
        self.us_as = 'AS15169 Google Inc.'
        self.us_ip = '64.233.161.99'
        self.us_hostname = 'google.com'

        self.gb_as = 'AS2818 BBC Internet Services, UK'
        self.gb_ip = '212.58.253.68'
        self.gb_hostname = 'bbc.com'

        self.gia = pygeoip.GeoIP(ASNUM_DB_PATH)

    def testOrgByAddr(self):
        gb_as = self.gia.org_by_addr(self.gb_ip)
        us_as = self.gia.org_by_addr(self.us_ip)

        self.assertEqual(gb_as, self.gb_as)
        self.assertEqual(us_as, self.us_as)

    def testOrgByName(self):
        gb_as = self.gia.org_by_name(self.gb_hostname)
        us_as = self.gia.org_by_name(self.us_hostname)

        self.assertEqual(gb_as, self.gb_as)
        self.assertEqual(us_as, self.us_as)

    @raises(pygeoip.GeoIPError)
    def testCodeByAddr(self):
        self.gia.country_code_by_addr(self.us_ip)

    @raises(pygeoip.GeoIPError)
    def testNameByAddr(self):
        self.gia.country_name_by_addr(self.us_ip)
