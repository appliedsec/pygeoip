# -*- coding: utf-8 -*-
import unittest

import pygeoip
from pygeoip import MEMORY_CACHE, MMAP_CACHE, STANDARD
from tests.config import COUNTRY_DB_PATH

class TestGeoIPCacheMethods(unittest.TestCase):
    def setUp(self):
        self.us_ip = '64.233.161.99'
        self.us_code = 'US'

        self.gi_mmap = pygeoip.GeoIP(COUNTRY_DB_PATH, MMAP_CACHE)
        self.gi_memory = pygeoip.GeoIP(COUNTRY_DB_PATH, MEMORY_CACHE)
        self.gi_standard = pygeoip.GeoIP(COUNTRY_DB_PATH, STANDARD)

    def testCountryCodeByAddr(self):
        code_mmap = self.gi_mmap.country_code_by_addr(self.us_ip)
        code_memory = self.gi_memory.country_code_by_addr(self.us_ip)
        code_standard = self.gi_standard.country_code_by_addr(self.us_ip)

        self.assertEqual(code_mmap, self.us_code)
        self.assertEqual(code_memory, self.us_code)
        self.assertEqual(code_standard, self.us_code)
