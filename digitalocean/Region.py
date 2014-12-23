# -*- coding: utf-8 -*-
from .baseapi import BaseAPI


class Region(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.name = None
        self.slug = None
        self.sizes = []
        self.available = None
        self.features = []
        super(Region, self).__init__(*args, **kwargs)

    def __str__(self):
        return "%s" % self.name
