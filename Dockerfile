# Dockerfile made to test this
FROM python:alpine

MAINTAINER Lorenzo Setale <lorenzo@setale.me>

RUN pip3 install -U python-digitalocean pytest

WORKDIR /root/python-digitalocean
ADD requirements.txt requirements.txt
RUN pip3 install -U -r requirements.txt

ADD . /root/python-digitalocean

CMD python3 -m pytest