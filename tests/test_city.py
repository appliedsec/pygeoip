# -*- coding: utf-8 -*-
import unittest

import pygeoip
from tests.config import CITY_DB_PATH


class TestGeoIPCityFunctions(unittest.TestCase):
    def setUp(self):
        self.us_hostname = 'google.com'
        self.us_ip = '64.233.161.99'

        self.gb_hostname = 'bbc.com'
        self.gb_ip = '212.58.253.68'

        self.us_code = 'US'
        self.gb_code = 'GB'

        self.us_name = 'United States'
        self.gb_name = 'United Kingdom'

        self.us_record_data = {
            'city': 'Mountain View',
            'region_code': 'CA',
            'longitude': -122.05740356445312,
            'country_code3': 'USA',
            'latitude': 37.419200897216797,
            'postal_code': '94043',
            'dma_code': 807,
            'area_code': 650,
            'metro_code': 'San Francisco, CA',
            'country_code': 'US',
            'country_name': 'United States',
            'continent': 'NA',
            'time_zone': 'America/Los_Angeles'
        }

        self.gb_record_data = {
            'city': 'Tadworth',
            'region_code': 'N7',
            'longitude': -0.23339999999998895,
            'country_code3': 'GBR',
            'latitude': 51.283299999999997,
            'postal_code': None,
            'dma_code': 0,
            'area_code': 0,
            'metro_code': None,
            'country_code': 'GB',
            'country_name': 'United Kingdom',
            'continent': 'EU',
            'time_zone': 'Europe/London'
        }

        self.us_region_data = {'region_code': 'CA', 'country_code': 'US'}
        self.gb_region_data = {'region_code': 'N7', 'country_code': 'GB'}

        self.gic = pygeoip.GeoIP(CITY_DB_PATH)
        self.gic_mem = pygeoip.GeoIP(CITY_DB_PATH, pygeoip.MEMORY_CACHE)
        self.gic_mmap = pygeoip.GeoIP(CITY_DB_PATH, pygeoip.MMAP_CACHE)

    def testCountryCodeByName(self):
        us_code = self.gic.country_code_by_name(self.us_hostname)
        gb_code = self.gic.country_code_by_name(self.gb_hostname)

        self.assertEqual(us_code, self.us_code)
        self.assertEqual(gb_code, self.gb_code)

    def testCountryCodeByAddr(self):
        us_code = self.gic.country_code_by_addr(self.us_ip)
        gb_code = self.gic.country_code_by_addr(self.gb_ip)

        self.assertEqual(us_code, self.us_code)
        self.assertEqual(gb_code, self.gb_code)

    def testCountryNameByName(self):
        us_name = self.gic.country_name_by_name(self.us_hostname)
        gb_name = self.gic.country_name_by_name(self.gb_hostname)

        self.assertEqual(us_name, self.us_name)
        self.assertEqual(gb_name, self.gb_name)

    def testCountryNameByAddr(self):
        us_name = self.gic.country_name_by_addr(self.us_ip)
        gb_name = self.gic.country_name_by_addr(self.gb_ip)

        self.assertEqual(us_name, self.us_name)
        self.assertEqual(gb_name, self.gb_name)

    def testRegionByName(self):
        us_region_data = self.gic.region_by_name(self.us_hostname)
        gb_region_data = self.gic.region_by_name(self.gb_hostname)

        self.assertEqual(us_region_data, self.us_region_data)
        self.assertEqual(gb_region_data, self.gb_region_data)

    def testRegionByAddr(self):
        us_region = self.gic.region_by_addr(self.us_ip)
        gb_region = self.gic.region_by_addr(self.gb_ip)

        self.assertEqual(us_region, self.us_region_data)
        self.assertEqual(gb_region, self.gb_region_data)

    def testCacheMethods(self):
        mem_record = self.gic_mem.record_by_addr(self.us_ip)
        mmap_record = self.gic_mmap.record_by_addr(self.us_ip)

        self.assertEqual(mem_record['city'], self.us_record_data['city'])
        self.assertEqual(mmap_record['city'], self.us_record_data['city'])

    def testRecordByAddr(self):
        equal_keys = ('city', 'region_name', 'area_code', 'country_code3',
                      'postal_code', 'dma_code', 'country_code', 'metro_code', 
                      'country_name', 'time_zone')
        almost_equal_keys = ('longitude', 'latitude')

        us_record = self.gic.record_by_addr(self.us_ip)
        for key, value in us_record.items():
            if key in equal_keys:
                test_value = self.us_record_data[key]
                self.assertEqual(value, test_value, 'Key: %s' % key)
            elif key in almost_equal_keys:
                test_value = self.us_record_data[key]
                self.assertAlmostEqual(value, test_value, 3, 'Key: %s' % key)

        gb_record = self.gic.record_by_addr(self.gb_ip)
        for key, value in gb_record.items():
            if key in equal_keys:
                test_value = self.gb_record_data[key]
                self.assertEqual(value, test_value, 'Key: %s' % key)
            elif key in almost_equal_keys:
                test_value = self.gb_record_data[key]
                self.assertAlmostEqual(value, test_value, 3, 'Key: %s' % key)

    def testRecordByName(self):
        equal_keys = ('city', 'region_name', 'area_code', 'country_code3',
                      'postal_code', 'dma_code', 'country_code',
                      'country_name', 'time_zone')
        almost_equal_keys = ('longitude', 'latitude')

        us_record = self.gic.record_by_name(self.us_hostname)
        for key, value in us_record.items():
            if key in equal_keys:
                test_value = self.us_record_data[key]
                self.assertEqual(value, test_value, 'Key: %s' % key)
            elif key in almost_equal_keys:
                test_value = self.us_record_data[key]
                self.assertAlmostEqual(value, test_value, 3, 'Key: %s' % key)

        gb_record = self.gic.record_by_name(self.gb_hostname)
        for key, value in gb_record.items():
            if key in equal_keys:
                test_value = self.gb_record_data[key]
                self.assertEqual(value, test_value, 'Key: %s' % key)
            elif key in almost_equal_keys:
                test_value = self.gb_record_data[key]
                self.assertAlmostEqual(value, test_value, 3, 'Key: %s' % key)
