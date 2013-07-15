Bootstrap manual for developers of pygeoip

Dependencies: tox, nose, epydoc

For testing we are using tox virtualenv-based Python version testing
and nose as test framwork.

Tox will create virtualenvs for all Python version pygeoip supports
and installs the current working tree using the setup.py install script.
Running the tests requires a couple of sample databases found on the
link below.

Maxmind sample databases for testing can be downloaded here:
http://www.defunct.cc/maxmind-geoip-samples.tar.gz (58 MB)

Extract the tarball in the tests directory and run tox from the root directory.

Please make sure your code passes all tests before opening pull requests.

All the best,
William Tisäter
