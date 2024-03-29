#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

long_description = """This library provides easy access to Digital Ocean APIs to deploy droplets, images and more."""

if os.path.isfile("DESCRIPTION.rst"):
    with open('DESCRIPTION.rst') as file:
        long_description = file.read()

setup(
    name='python-digitalocean',
    version='1.17.0',
    description='digitalocean.com API to manage Droplets and Images',
    author='Lorenzo Setale ( http://who.is.lorenzo.setale.me/? )',
    author_email='lorenzo@setale.me',
    url='https://github.com/koalalorenzo/python-digitalocean',
    packages=['digitalocean'],
    install_requires=['requests', 'jsonpickle'],
    test_suite='digitalocean.tests',
    license='LGPL v3',
    long_description=long_description
)
