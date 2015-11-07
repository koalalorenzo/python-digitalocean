# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT


class Image(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.name = None
        self.distribution = None
        self.slug = None
        self.min_size = None
        self.public = None
        self.regions = []
        self.created_at = None

        super(Image, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, image_id, mocked):
        """
            Class method that will return an Image object by ID.
        """
        image = cls(token=api_token, id=image_id, mocked=mocked)
        image.mock_data = "images/single.json"
        image.load()
        return image

    def load(self):
        data = self.get_data("images/%s" % self.id)
        image_dict = data['image']

        # Setting the attribute values
        for attr in image_dict.keys():
            setattr(self, attr, image_dict[attr])

        return self

    def destroy(self):
        """
            Destroy the image
        """
        self.mock_status = 204
        return self.get_data("images/%s/" % self.id, type=DELETE)

    def transfer(self, new_region_slug):
        """
            Transfer the image
        """
        self.mock_data = "actions/ipv6_completed.json" 
        return self.get_data(
            "images/%s/actions/" % self.id,
            type=POST,
            params={"type": "transfer", "region": new_region_slug}
        )

    def rename(self, new_name):
        """
            Rename an image
        """
        self.mock_data = "actions/ipv6_completed.json" 
        return self.get_data(
            "images/%s" % self.id,
            type=PUT,
            params={"name": new_name}
        )

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.distribution)

    def __repr__(self):
        return "< %s %s %s >" % (self.id, self.distribution, self.name)
