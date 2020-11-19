clean:
	rm -rf build 
	rm -rf dist 
	rm -rf python_digitalocean.egg-info 
	rm -rf .pytest_cache
.PHONY: clean

dist:

build:
	
deps:
	pip install -U -r requirements.txt
.PHONY: deps

test:
	python -m pytest
.PHONY: test

