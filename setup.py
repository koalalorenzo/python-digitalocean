#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

long_description = """python-digitalocean is a python package that provide easy access to digitalocean.com APIs to manage droplets, images and more."""

if os.path.isfile("README.md"):
    with open('README.md') as file:
        long_description = file.read()

setup(name='python-digitalocean',
<<<<<<< HEAD
      version='0.2.7',
=======
<<<<<<< HEAD
      version='0.2.5',
=======
      version='0.2.6',
>>>>>>> 528237d2006ef980eb4e49ca9c669f9f627e98b4
>>>>>>> rdgreis-master
      description='digitalocean.com API to manage Droplets and Images',
      author='Lorenzo Setale ( http://who.is.lorenzo.setale.me/? )',
      author_email='koalalorenzo@gmail.com',
      url='https://github.com/koalalorenzo/python-digitalocean',
      packages=['digitalocean'],
      install_requires=['requests'],
      long_description=long_description
     )
