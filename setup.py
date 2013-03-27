#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

long_description = """python-digitalocean is a python package that provide easy acces to digitalocean.com APIs to manage droplets, images and more."""

if os.path.isfile("README.md"):
    with open('README.md') as file:
        long_description = file.read()

setup(name='python-digitalocean',
      version='0.2.3',
      description='digitalocean.com API to manage Droplets and Images',
      author='Lorenzo Setale ( http://who.is.koalalorenzo.com/? )',
      author_email='koalalorenzo@gmail.com',
      url='https://github.com/koalalorenzo/python-digitalocean',
      packages=['digitalocean'],
      long_description=long_description
     )
