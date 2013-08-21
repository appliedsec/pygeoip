import os.path as path

DATA_DIR = path.join(path.dirname(path.realpath(__file__)), 'data')

COUNTRY_DB_PATH = path.join(DATA_DIR, 'GeoIP.dat')
COUNTRY_V6_DB_PATH = path.join(DATA_DIR, 'GeoIPv6.dat')
REGION_DB_PATH = path.join(DATA_DIR, 'GeoIPRegion.dat')
CITY_DB_PATH = path.join(DATA_DIR, 'GeoLiteCity.dat')
ORG_DB_PATH = path.join(DATA_DIR, 'GeoIPOrg.dat')
ASNUM_DB_PATH = path.join(DATA_DIR, 'GeoIPASNum.dat')
ISP_DB_PATH = path.join(DATA_DIR, 'GeoIPISP.dat')
CORRUPT_DB_PATH = path.join(DATA_DIR, '../config.py')
