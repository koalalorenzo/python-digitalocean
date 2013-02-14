#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='python-digitalocean',
      version='0.2.1',
      description='digitalocean.com API to manage Droplets and Images',
      author='Lorenzo Setale ( http://who.is.koalalorenzo.com/? )',
      author_email='koalalorenzo@gmail.com',
      url='https://github.com/koalalorenzo/python-digitalocean',
      packages=['digitalocean'],
      long_description=long_description
     )