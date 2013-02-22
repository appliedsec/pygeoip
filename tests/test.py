# -*- coding: utf-8 -*-
import unittest

from pygeoip import const

class TestSanity(unittest.TestCase):
    def testConstLengths(self):
        assert len(const.COUNTRY_CODES) == len(const.COUNTRY_CODES3)
        assert len(const.COUNTRY_CODES) == len(const.COUNTRY_NAMES)
        assert len(const.COUNTRY_CODES) == len(const.CONTINENT_NAMES)
