# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT


class Image(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.name = None
        self.distribution = None
        self.slug = None
        self.min_disk_size = None
        self.public = None
        self.regions = []
        self.created_at = None
        self.size_gigabytes = None

        super(Image, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, image_id_or_slug):
        """
            Class method that will return an Image object by ID or slug.
        """
        try:
            int(image_id_or_slug)
            image = cls(token=api_token, id=image_id_or_slug)
        except ValueError:
            image = cls(token=api_token, slug=image_id_or_slug)
            image.load(use_slug=use_slug)
        else:
        return image

    def load(self, use_slug=False):
        """
            Load slug.

            Loads by id unless use_slug is True.
        """
        if (use_slug and self.slug):
            identifier = self.slug
        else:
            identifier = self.id
        data = self.get_data("images/%s" % identifier)
        image_dict = data['image']

        # Setting the attribute values
        for attr in image_dict.keys():
            setattr(self, attr, image_dict[attr])

        return self

    def destroy(self):
        """
            Destroy the image
        """
        return self.get_data("images/%s/" % self.id, type=DELETE)

    def transfer(self, new_region_slug):
        """
            Transfer the image
        """
        return self.get_data(
            "images/%s/actions/" % self.id,
            type=POST,
            params={"type": "transfer", "region": new_region_slug}
        )

    def rename(self, new_name):
        """
            Rename an image
        """
        return self.get_data(
            "images/%s" % self.id,
            type=PUT,
            params={"name": new_name}
        )

    def __str__(self):
        return "<Image: %s %s %s>" % (self.id, self.distribution, self.name)
