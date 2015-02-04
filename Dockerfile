# Dokcerfile made to test this
FROM ubuntu:14.04

MAINTAINER Lorenzo Setale <koalalorenzo@gmail.com>

RUN apt-get update
RUN apt-get install --yes git python-dev python-pip
RUN pip install -U pip

RUN pip install -U python-digitalocean pytest

WORKDIR /root/
RUN git clone https://github.com/koalalorenzo/python-digitalocean.git

WORKDIR /root/python-digitalocean
RUN pip install -U -r requirements.txt
RUN py.test