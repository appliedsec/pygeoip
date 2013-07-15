# ChangeLog for pygeoip

### Release 0.2.7

* New: Added support for IPv6 ASN and City databases
* Fix: Sync timezones from latest ISO-8601 edition
* Fix: `record_by_addr()` will now return `None` when missing data

[William Tisäter](mailto:william@defunct.cc) -- 2013-06-04 15:55:01

### Release 0.2.6

* New: Python 3.3 support
* New: IPv6 support
* New: Added `continent` key to region lookup
* New: Catch all database parse errors as `GeoIPError('Corrupt database')`
* Fix: Handle empty responses from `_get_record`
* Fix: Rename some countries to modern names
* Fix: Add new country codes for SS, BQ (Thanks to Todd Federman)
* Fix: Ship metadata with source distribution (Thanks to ralphbean)
* Fix: Simplify ip2long methods (Thanks to stevetu)
* Fix: Encoding bug when reading CityLite from mmap or memory
* Fix: Remove `__future__` imports
* Fix: Better PEP8 compatibility
* Fix: Switched from DOS to UNIX file format
* Fix: Misspelled countries (Thanks to Erik Fichtner)
* Fix: Dropped dependencies to six
* Fix: Optimize and refactor internal seek functions
* Fix: Make StringIO work with Python 3
* Fix: Remove dependency of ez_setup.py
* Fix: Add Python 3.2 and 3.3 to tox tests

[William Tisäter](mailto:william@defunct.cc) -- 2013-02-22 02:51:36

