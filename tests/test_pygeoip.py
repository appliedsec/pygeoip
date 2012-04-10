from __future__ import with_statement, absolute_import
import unittest

import pygeoip

from .config import (CITY_DB_PATH, COUNTRY_DB_PATH, ISP_DB_PATH, ORG_DB_PATH, REGION_DB_PATH, _data_dir)

class BaseGeoIPTestCase(unittest.TestCase):
    def setUp(self):
        self.us_hostname = 'google.com'
        self.us_ip = '64.233.161.99'
        self.gb_hostname = 'bbc.com'
        self.gb_ip = '212.58.253.68'

        self.yahoo_hostname = 'yahoo.com'
        self.yahoo_ip = '209.131.36.159'
        self.yahoo_region_data = {'region_name': 'CA', 'country_code': 'US'}

        self.us_code = 'US'
        self.gb_code = 'GB'
        self.us_name = 'United States'
        self.gb_name = 'United Kingdom'

        self.us_code3 = 'USA'
        self.gb_code3 = 'GBR'

        self.google_record_data = {'city': 'Mountain View',
                                   'region_name': 'CA',
                                   'area_code': 650,
                                   'longitude': -122.05740356445312,
                                   'country_code3': 'USA',
                                   'latitude': 37.419200897216797,
                                   'postal_code': '94043',
                                   'dma_code': 807,
                                   'country_code': 'US',
                                   'country_name': 'United States',
                                   'time_zone': 'America/Los_Angeles'}

        self.bbc_record_data = {'city': 'Tadworth',
                                'region_name': 'N7',
                                'area_code': 0,
                                'longitude': -0.23339999999998895,
                                'country_code3': 'GBR',
                                'latitude': 51.283299999999997,
                                'postal_code': None, 'dma_code': 0,
                                'country_code': 'GB',
                                'country_name': 'United Kingdom',
                                'time_zone': 'Europe/London'}

        self.bbc_record_data_by_addr = {'city': 'Tadworth',
                                'region_name': 'N7',
                                'area_code': 0,
                                'longitude': -0.23339999999998895,
                                'country_code3': 'GBR',
                                'latitude': 51.283299999999997,
                                'postal_code': None, 'dma_code': 0,
                                'country_code': 'GB',
                                'country_name': 'United Kingdom',
                                'time_zone': 'Europe/London'}

        self.google_region_data = {'region_name': 'CA', 'country_code': 'US'}
        self.bbc_region_data = {'region_name': 'N7', 'country_code': 'GB'}

        self.google_org = 'Google'
        self.bbc_org = 'BBC'


class TestGeoIPCountryFunctions(BaseGeoIPTestCase):

    def setUp(self):
        super(TestGeoIPCountryFunctions, self).setUp()
        self.gi = pygeoip.GeoIP(COUNTRY_DB_PATH)
        self.gic = pygeoip.GeoIP(CITY_DB_PATH)
        self.gir = pygeoip.GeoIP(REGION_DB_PATH)

    def testCountryCodeByName(self):
        self.assertEqual(self.gi.country_code_by_name(self.us_hostname), self.us_code)
        self.assertEqual(self.gi.country_code_by_name(self.gb_hostname), self.gb_code)
        self.assertEqual(self.gic.country_code_by_name(self.us_hostname), self.us_code)
        self.assertEqual(self.gic.country_code_by_name(self.gb_hostname), self.gb_code)
        self.assertEqual(self.gir.country_code_by_name(self.yahoo_hostname), self.us_code)

    def testCountryCodeByAddr(self):
        self.assertEqual(self.gi.country_code_by_addr(self.us_ip), self.us_code)
        self.assertEqual(self.gi.country_code_by_addr(self.gb_ip), self.gb_code)
        self.assertEqual(self.gic.country_code_by_addr(self.us_ip), self.us_code)
        self.assertEqual(self.gic.country_code_by_addr(self.gb_ip), self.gb_code)
        self.assertEqual(self.gir.country_code_by_addr(self.yahoo_ip), self.us_code)

    def testCountryNameByName(self):
        self.assertEqual(self.gi.country_name_by_name(self.us_hostname), self.us_name)
        self.assertTrue(self.gi.country_name_by_name(self.gb_hostname).startswith(self.gb_name))
        self.assertEqual(self.gic.country_name_by_name(self.us_hostname), self.us_name)
        self.assertTrue(self.gic.country_name_by_name(self.gb_hostname).startswith(self.gb_name))

    def testCountryNameByAddr(self):
        self.assertEqual(self.gi.country_name_by_addr(self.us_ip), self.us_name)
        self.assertTrue(self.gi.country_name_by_addr(self.gb_ip).startswith(self.gb_name))
        self.assertEqual(self.gic.country_name_by_addr(self.us_ip), self.us_name)
        self.assertTrue(self.gic.country_name_by_addr(self.gb_ip).startswith(self.gb_name))

class TestGeoIPOrgFunctions(BaseGeoIPTestCase):
    def setUp(self):
        super(TestGeoIPOrgFunctions, self).setUp()
        self.gi = pygeoip.GeoIP(ORG_DB_PATH)

    def testOrgByAddr(self):
        self.assertTrue(self.gi.org_by_addr(self.gb_ip).startswith(self.bbc_org))
        self.assertEqual(self.gi.org_by_addr(self.us_ip), self.google_org)

    def testOrgByName(self):
        self.assertTrue(self.gi.org_by_name(self.gb_hostname).startswith(self.bbc_org))
        self.assertEqual(self.gi.org_by_name(self.us_hostname), self.google_org)

class TestGeoIPRecordFunctions(BaseGeoIPTestCase):
    def setUp(self):
        super(TestGeoIPRecordFunctions, self).setUp()
        self.gi = pygeoip.GeoIP(CITY_DB_PATH)

    def testRecordByAddr(self):
        equal_keys = ('city', 'region_name', 'area_code', 'country_code3',
                      'postal_code', 'dma_code', 'country_code', 'country_name',
                      'time_zone')
        almost_equal_keys = ('longitude', 'latitude')

        google_record = self.gi.record_by_addr(self.us_ip)

        for key, value in google_record.items():
            if key in equal_keys:
                self.assertEqual(value, self.google_record_data[key], 'Key: %s' % key)
            elif key in almost_equal_keys:
                self.assertAlmostEqual(value, self.google_record_data[key], 3, 'Key: %s' % key)

        bbc_record = self.gi.record_by_addr(self.gb_ip)

        print(bbc_record)

        for key, value in bbc_record.items():
            if key in equal_keys:
                self.assertEqual(value, self.bbc_record_data_by_addr[key], 'Key: %s, Test value: %s, Actual value: %s' % (key, self.bbc_record_data_by_addr[key], value))
            elif key in almost_equal_keys:
                self.assertAlmostEqual(value, self.bbc_record_data_by_addr[key], 3, 'Key: %s' % key)

    def testRecordByName(self):
        equal_keys = ('city', 'region', 'area_code', 'country_code3',
                      'postal_code', 'dma_code', 'country_code', 'country_name',
                      'time_zone')
        almost_equal_keys = ('longitude', 'latitude')

        google_record = self.gi.record_by_name(self.us_hostname)

        for key, value in google_record.items():
            if key in equal_keys:
                self.assertEqual(value, self.google_record_data[key], 'Key: %s' % key)
            elif key in almost_equal_keys:
                self.assertAlmostEqual(value, self.google_record_data[key], 3, 'Key: %s' % key)

        bbc_record = self.gi.record_by_name(self.gb_hostname)

        print(bbc_record)

        for key, value in bbc_record.items():
            if key in equal_keys:
                self.assertEqual(value, self.bbc_record_data[key])
            elif key in almost_equal_keys:
                self.assertAlmostEqual(value, self.bbc_record_data[key], 3, 'Key: %s, Test value: %s, Actual value: %s' % (key, self.bbc_record_data[key], value))

    def testTimeZoneByAddr(self):
        google_time_zone = self.gi.time_zone_by_addr(self.us_ip)
        self.assertEquals(google_time_zone, 'America/Los_Angeles')

        bbc_time_zone = self.gi.time_zone_by_addr(self.gb_ip)
        self.assertEquals(bbc_time_zone, 'Europe/London')

    def testTimeZoneByName(self):
        google_time_zone = self.gi.time_zone_by_name(self.us_hostname)
        self.assertEquals(google_time_zone, 'America/Los_Angeles')

        bbc_time_zone = self.gi.time_zone_by_name(self.gb_hostname)
        self.assertEquals(bbc_time_zone, 'Europe/London')

class TestGeoIPRegionFunctions(BaseGeoIPTestCase):
    def setUp(self):
        super(TestGeoIPRegionFunctions, self).setUp()
        self.gic = pygeoip.GeoIP(CITY_DB_PATH)
        self.gir = pygeoip.GeoIP(REGION_DB_PATH)

    def testRegionByNameCityDB(self):
        self.assertEqual(self.gic.region_by_name(self.us_hostname), self.google_region_data)
        self.assertEqual(self.gic.region_by_name(self.gb_hostname), self.bbc_region_data)

        self.assertEqual(self.gir.region_by_name(self.yahoo_hostname), self.yahoo_region_data)

    def testRegionByAddrCityDB(self):
        self.assertEqual(self.gic.region_by_addr(self.us_ip), self.google_region_data)
        self.assertEqual(self.gic.region_by_addr(self.gb_ip), {'region_name': 'N7', 'country_code': 'GB'})

        self.assertEqual(self.gir.region_by_addr(self.yahoo_ip), self.yahoo_region_data)

if __name__ == '__main__':
    unittest.main()
