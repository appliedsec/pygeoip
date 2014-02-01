# -*- coding: utf-8 -*-
import sys
import unittest
import threading

import pygeoip
from tests.config import COUNTRY_DB_PATH


class TestGeoIPThreading(unittest.TestCase):
    def setUp(self):
        self.gi = pygeoip.GeoIP(COUNTRY_DB_PATH)

    def testCountryDatabase(self):
        t1 = TestThread('us', '64.17.254.216', 'US', self)
        t2 = TestThread('it', '78.26.70.208', 'IT', self)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        if t1.exc_info:
            raise t1.exc_info[1]

        if t2.exc_info:
            raise t2.exc_info[1]


class TestThread(threading.Thread):
    def __init__(self, name, ip, code, test):
        threading.Thread.__init__(self, name=name)
        self.ip = ip
        self.code = code
        self.test = test
        self.exc_info = None

    def run(self):
        try:
            for i in range(1000):
                code = self.test.gi.country_code_by_addr(self.ip)
                self.test.assertEqual(code, self.code)
        except AssertionError:
            self.exc_info = sys.exc_info()
