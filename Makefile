.PHONY: docs

all: test

test:
	@echo "Downloading test databases"
	rm -rf maxmind-geoip-samples.tar.gz tests/data; mkdir -p tests/data
	curl -s https://www.defunct.cc/maxmind-geoip-samples.tar.gz | tar -zx -C tests
	
	@echo "Testing local state"
	@tox --version > /dev/null || (echo "Requires tox - install requirements.txt"; exit 1)
	tox

docs:
	@echo "Building documentation"
	make -C docs clean
	make -C docs html

clean:
	@echo "Cleaning doc, test and cache files"
	git clean -fd
	find . -name *.pyc -delete
	rm -rf pygeoip-* pygeoip.egg-info

