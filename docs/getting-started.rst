Getting Started
===============

Create your GeoIP instance with appropriate access flag. ``STANDARD``
reads data from disk when needed, ``MEMORY_CACHE`` loads database into
memory on instantiation and ``MMAP_CACHE`` loads database into memory
using mmap.

.. code:: python

    >>> import pygeoip
    >>> gi = pygeoip.GeoIP('GeoIP.dat')
    >>> gi.country_name_by_addr('64.233.161.99')
    'United States'

Country Lookup
--------------

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIP.dat')
    >>> gi.country_code_by_name('google.com')
    'US'
    >>> gi.country_code_by_addr('64.233.161.99')
    'US'
    >>> gi.country_name_by_addr('64.233.161.99')
    'United States'

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIPv6.dat')
    >>> gi.country_code_by_addr('2a00:1450:400f:802::1006')
    'IE'

Region Lookup
-------------

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIPRegion.dat')
    >>> gi.region_by_name('apple.com')
    {'region_code': 'CA', 'country_code': 'US'}

City Lookup
-----------

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIPCity.dat')
    >>> gi.record_by_addr('64.233.161.99')
    {
        'city': u'Mountain View',
        'region_code': u'CA',
        'area_code': 650,
        'time_zone': 'America/Los_Angeles',
        'dma_code': 807,
        'metro_code': 'San Francisco, CA',
        'country_code3': 'USA',
        'latitude': 37.41919999999999,
        'postal_code': u'94043',
        'longitude': -122.0574,
        'country_code': 'US',
        'country_name': 'United States',
        'continent': 'NA'
    }
    >>> gi.time_zone_by_addr('64.233.161.99')
    'America/Los_Angeles'

Organization Lookup
-------------------

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIPOrg.dat')
    >>> gi.org_by_name('dell.com')
    'Dell Computer Corporation'

ISP Lookup
----------

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIPISP.dat')
    >>> gi.isp_by_name('cnn.com')
    'Turner Broadcasting System'

ASN Lookup
----------

.. code:: python

    >>> gi = pygeoip.GeoIP('GeoIPASNum.dat')
    >>> gi.asn_by_name('cnn.com')
    'AS5662 Turner Broadcasting'
