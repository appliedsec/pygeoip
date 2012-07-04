import os

_data_dir = os.path.join(os.getcwd() , "data")

COUNTRY_DB_PATH = os.path.join(_data_dir, 'GeoIP.dat')
ISP_DB_PATH = os.path.join(_data_dir, 'GeoIPISP.dat')
ORG_DB_PATH = os.path.join(_data_dir, 'GeoIPOrg.dat')
CITY_DB_PATH = os.path.join(_data_dir, 'GeoLiteCity.dat')
REGION_DB_PATH = os.path.join(_data_dir, 'GeoIPRegion-515.dat')
