# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import REGION_DB_PATH


class TestGeoIPRegionFunctions(unittest.TestCase):
    def setUp(self):
        self.se_hostname = 'dn.se'
        self.se_region_data = {
            'region_code': None,
            'country_code': None
        }

        self.ca_hostname = 'cbc.ca'
        self.ca_region_data = {
            'region_code': 'ON',
            'country_code': 'CA'
        }

        self.us_code = 'US'
        self.us_hostname = 'apple.com'
        self.us_ip = '17.172.224.47'
        self.us_region_data = {
            'region_code': 'CA',
            'country_code': 'US'
        }

        self.gir = pygeoip.GeoIP(REGION_DB_PATH)

    def testRegionByName(self):
        region_name = self.gir.region_by_name(self.us_hostname)
        self.assertEqual(region_name, self.us_region_data)

    def testRegionByAddr(self):
        region_name = self.gir.region_by_addr(self.us_ip)
        self.assertEqual(region_name, self.us_region_data)

    def testCountryCodeByName(self):
        us_code = self.gir.country_code_by_name(self.us_hostname)
        self.assertEqual(us_code, self.us_code)

    def testCountryCodeByAddr(self):
        us_code = self.gir.country_code_by_addr(self.us_ip)
        self.assertEqual(us_code, self.us_code)

    def testCanadaRegion(self):
        region_name = self.gir.region_by_name(self.ca_hostname)
        self.assertEqual(region_name, self.ca_region_data)

    def testSwedenRegion(self):
        region_name = self.gir.region_by_name(self.se_hostname)
        self.assertEqual(region_name, self.se_region_data)
