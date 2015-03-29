# Dokcerfile made to test this
FROM ubuntu:14.04

MAINTAINER Lorenzo Setale <koalalorenzo@gmail.com>

RUN apt-get update
RUN apt-get install --yes git python3-dev python3-pip python-dev python-pip
RUN pip3 install -U pip
RUN pip2 install -U pip

RUN pip3 install -U python-digitalocean pytest
RUN pip2 install -U python-digitalocean pytest

WORKDIR /root/
ADD . /root/python-digitalocean

WORKDIR /root/python-digitalocean
RUN pip2 install -U -r requirements.txt
RUN pip3 install -U -r requirements.txt

CMD py.test-2.7 ; py.test-3.4