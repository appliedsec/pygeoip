# ChangeLog for pygeoip

### Release 0.3.2

* New: Support for Python 3.4
* New: Support for NetSpeedCell databases (Thanks to Gregory Oschwald)
* Fix: Improved exception handling (Thanks to Oliver Keyes)
* Fix: Return country for region lookups outside US and CA

Not yet uploaded to PyPi

### Release 0.3.1

* New: Documentation now available on readthedocs.org
* New: MaxMind Netspeed database support
* Fix: Release thread lock on exceptions

Uploaded to PyPi on 2014-02-05

### Release 0.3.0

* New: 100% test coverage
* New: Dropped Python 3.1 support
* New: Add reStructuredText version of README for PyPI
* New: Add `last_netmask` function and return the netmask depth of the last lookup
* Fix: Rename `region_name` to `region_code` (returned by `region_by_name` and `record_by_addr`)
* Fix: Rename `id_by_addr` to `_id_by_addr`
* Fix: Make internal meta class private
* Fix: Support caching on class inheritance (Thanks to Jiří Techet)
* Fix: Properly open databases on GAE (Thanks to Jiří Techet)
* Fix: Treat IndexError and UnicodeDecodeError as corrupt database and raise others (Thanks to Jiří Techet)
* Fix: Aquire lock on instance creation (Thanks to Jiří Techet)
* Fix: Fixed alpha-3 codes ordering, replaced TLS,TKM,TUN,TON with TKM,TUN,TON,TLS (Thanks to Marc Sherry)

Uploaded to PyPi on 2013-11-13

### Release 0.2.7

* New: Added support for IPv6 ASN and City databases
* Fix: Sync timezones from latest ISO-8601 edition
* Fix: `record_by_addr()` will now return `None` when missing data

Uploaded to PyPi on 2013-07-15

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

Uploaded to PyPi on 2013-02-23
