# -*- coding: utf-8 -*-
from .baseapi import BaseAPI

class Metadata(BaseAPI):
    droplet_id = None
    end_point = "http://169.254.169.254/metadata/v1"

    def __init__(self, *args, **kwargs):
        super(Metadata, self).__init__(*args, **kwargs)
        self.end_point = "http://169.254.169.254/metadata/v1"

    def load(self):
        metadata = self.get_data(".json")

        for attr in metadata.keys():
            setattr(self,attr,metadata[attr])

        return self

    def __str__(self):
        return "%s" % self.droplet_id