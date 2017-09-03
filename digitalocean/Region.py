# -*- coding: utf-8 -*-
from .baseapi import BaseAPI


NYC1 = 'nyc1'
NYC2 = 'nyc2'
NYC3 = 'nyc3'
SFO1 = 'sfo1'
SFO2 = 'sfo2'
AMS2 = 'ams2'
AMS3 = 'ams3'
LON1 = 'lon1'
SGP1 = 'sgp1'
FRA1 = 'fra1'
TOR1 = 'tor1'
BLR1 = 'blr1'


class Region(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.name = None
        self.slug = None
        self.sizes = []
        self.available = None
        self.features = []
        super(Region, self).__init__(*args, **kwargs)

    def __str__(self):
        return "<Region: %s %s>" % (self.slug, self.name)
