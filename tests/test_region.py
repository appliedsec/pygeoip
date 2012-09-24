# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import REGION_DB_PATH


class TestGeoIPRegionFunctions(unittest.TestCase):
    def setUp(self):
        self.us_code = 'US'

        self.yahoo_hostname = 'yahoo.com'
        self.yahoo_ip = '209.131.36.159'
        self.yahoo_region_data = {
            'region_name': 'CA',
            'country_code': 'US'
        }

        self.gir = pygeoip.GeoIP(REGION_DB_PATH)

    def testRegionByName(self):
        region_name = self.gir.region_by_name(self.yahoo_hostname)
        self.assertEqual(region_name, self.yahoo_region_data)

    def testRegionByAddr(self):
        region_name = self.gir.region_by_addr(self.yahoo_ip)
        self.assertEqual(region_name, self.yahoo_region_data)

    def testCountryCodeByName(self):
        us_code = self.gir.country_code_by_name(self.yahoo_hostname)
        self.assertEqual(us_code, self.us_code)

    def testCountryCodeByAddr(self):
        us_code = self.gir.country_code_by_addr(self.yahoo_ip)
        self.assertEqual(us_code, self.us_code)
