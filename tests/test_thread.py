# -*- coding: utf-8 -*-
import unittest
import threading

import pygeoip
from tests.config import COUNTRY_DB_PATH


class TestGeoIPThreading(unittest.TestCase):
    def setUp(self):
        self.us_ip = '64.233.161.99'
        self.gb_ip = '212.58.253.68'

        self.us_code = 'US'
        self.gb_code = 'GB'

        self.gi = pygeoip.GeoIP(COUNTRY_DB_PATH)

    def testCountryDatabase(self):
        us_thread = TestThread('us', self.gi, self.us_ip, self.us_code, self.assertEqual)
        gb_thread = TestThread('gb', self.gi, self.us_ip, self.us_code, self.assertEqual)
        us_thread.start()
        gb_thread.start()
        us_thread.join()
        gb_thread.join()


class TestThread(threading.Thread):
    def __init__(self, name, gi, ip, code, assertEqual):
        threading.Thread.__init__(self, name=name)
        self.ip = ip
        self.gi = gi
        self.code = code
        self.assertEqual = assertEqual

    def run(self):
        for i in range(1000):
            code = self.gi.country_code_by_addr(self.ip)
            self.assertEqual(code, self.code)
