# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import COUNTRY_DB_PATH


class TestGeoIPCountryFunctions(unittest.TestCase):
    def setUp(self):
        self.us_hostname = 'google.com'
        self.gb_hostname = 'bbc.com'

        self.us_ip = '64.233.161.99'
        self.gb_ip = '212.58.253.68'

        self.us_code = 'US'
        self.gb_code = 'GB'

        self.us_name = 'United States'
        self.gb_name = 'United Kingdom'

        self.gi = pygeoip.GeoIP(COUNTRY_DB_PATH)

    def testCountryCodeByName(self):
        us_code = self.gi.country_code_by_name(self.us_hostname)
        gb_code = self.gi.country_code_by_name(self.gb_hostname)

        self.assertEqual(us_code, self.us_code)
        self.assertEqual(gb_code, self.gb_code)

    def testCountryCodeByAddr(self):
        us_code = self.gi.country_code_by_addr(self.us_ip)
        gb_code = self.gi.country_code_by_addr(self.gb_ip)
        
        self.assertEqual(us_code, self.us_code)
        self.assertEqual(gb_code, self.gb_code)

    def testCountryNameByName(self):
        us_name = self.gi.country_name_by_name(self.us_hostname)
        gb_name = self.gi.country_name_by_name(self.gb_hostname)

        self.assertEqual(us_name, self.us_name)
        self.assertEqual(gb_name, self.gb_name)

    def testCountryNameByAddr(self):
        us_name = self.gi.country_name_by_addr(self.us_ip)
        gb_name = self.gi.country_name_by_addr(self.gb_ip)

        self.assertEqual(us_name, self.us_name)
        self.assertEqual(gb_name, self.gb_name)
