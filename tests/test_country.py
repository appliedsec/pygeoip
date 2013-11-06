# -*- coding: utf-8 -*-
import socket
import unittest
from nose.tools import raises

import pygeoip
from tests.config import COUNTRY_DB_PATH, COUNTRY_V6_DB_PATH


class TestGeoIPCountryFunctions(unittest.TestCase):
    def setUp(self):
        self.us_hostname = 'google.com'
        self.gb_hostname = 'bbc.com'

        self.us_ip = '64.233.161.99'
        self.gb_ip = '212.58.253.68'

        self.ie6_hostname = 'ipv6.loopia.se'
        self.ie6_ip = '2a00:1450:400f:800::1002'

        self.ie_code = 'IE'
        self.us_code = 'US'
        self.gb_code = 'GB'
        self.se_code = 'SE'

        self.ie_name = 'Ireland'
        self.us_name = 'United States'
        self.gb_name = 'United Kingdom'
        self.se_name = 'Sweden'

        self.gi = pygeoip.GeoIP(COUNTRY_DB_PATH)
        self.gi6 = pygeoip.GeoIP(COUNTRY_V6_DB_PATH)

    def testCountryCodeByName(self):
        us_code = self.gi.country_code_by_name(self.us_hostname)
        gb_code = self.gi.country_code_by_name(self.gb_hostname)
        ie6_code = self.gi6.country_code_by_name(self.ie6_hostname)

        self.assertEqual(us_code, self.us_code)
        self.assertEqual(gb_code, self.gb_code)
        self.assertEqual(ie6_code, self.se_code)

    def testCountryCodeByAddr(self):
        us_code = self.gi.country_code_by_addr(self.us_ip)
        gb_code = self.gi.country_code_by_addr(self.gb_ip)
        ie6_code = self.gi6.country_code_by_addr(self.ie6_ip)

        self.assertEqual(us_code, self.us_code)
        self.assertEqual(gb_code, self.gb_code)
        self.assertEqual(ie6_code, self.ie_code)

    def testCountryNameByName(self):
        us_name = self.gi.country_name_by_name(self.us_hostname)
        gb_name = self.gi.country_name_by_name(self.gb_hostname)
        ie6_name = self.gi6.country_name_by_name(self.ie6_hostname)

        self.assertEqual(us_name, self.us_name)
        self.assertEqual(gb_name, self.gb_name)
        self.assertEqual(ie6_name, self.se_name)

    def testCountryNameByAddr(self):
        us_name = self.gi.country_name_by_addr(self.us_ip)
        gb_name = self.gi.country_name_by_addr(self.gb_ip)
        ie6_name = self.gi6.country_name_by_addr(self.ie6_ip)

        self.assertEqual(us_name, self.us_name)
        self.assertEqual(gb_name, self.gb_name)
        self.assertEqual(ie6_name, self.ie_name)

    @raises(pygeoip.GeoIPError)
    def testOpen4With6(self):
        data = self.gi.country_code_by_addr(self.ie6_ip)
        raise ValueError(data)

    @raises(pygeoip.GeoIPError)
    def testOpen6With4(self):
        data = self.gi6.country_code_by_addr(self.gb_ip)
        raise ValueError(data)

    @raises(pygeoip.GeoIPError)
    def testOrgByAddr(self):
        self.gi.org_by_addr(self.us_ip)

    @raises(pygeoip.GeoIPError)
    def testRecordByAddr(self):
        self.gi.record_by_addr(self.us_ip)

    @raises(pygeoip.GeoIPError)
    def testRegionByAddr(self):
        self.gi.region_by_addr(self.us_ip)

    @raises(pygeoip.GeoIPError)
    def testTimeZoneByAddr(self):
        self.gi.time_zone_by_addr(self.us_ip)
