clean:
	rm -rf build 
	rm -rf dist 
	rm -rf python_digitalocean.egg-info 
	rm -rf .pytest_cache
.PHONY: clean

dist:
	python setup.py sdist bdist_wheel

publish: dist
	twine upload dist/*
.PHONY: publish

publish_deps:
	python -m pip install --upgrade pip
	pip install setuptools wheel twine
.PHONY: publish_deps

deps:
	pip install -U -r requirements.txt
.PHONY: deps

test:
	python -m pytest
.PHONY: test

