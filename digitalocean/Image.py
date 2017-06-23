# -*- coding: utf-8 -*-
import re

from .baseapi import BaseAPI, POST, DELETE, PUT, NotFoundError

IMAGE_SERIAL_NO = re.compile('^\d{7}$')


def looks_like_image_id(image_id_or_slug, max=10):
    """
    Does this resemble an image_id?

    Returns True if it does.

    As of images ids are all 7 digit integers, but these are a quarter used up.
    A default limit of 10 digits is applied, to allow for edge cases like
    serial numbers being supplied as slugs.

    Note this is not guaranteed to work, the Digital Ocean REST api
    enddpoint to get an image is the same whether you use an id or slug,
    so there are obvious issues with using numbers as slugs.
    """
    match = False
    image_id_or_slug = str(image_id_or_slug)
    if re.match(
            IMAGE_SERIAL_NO, image_id_or_slug
    ) and len(image_id_or_slug) <= max:
        match = True
    return match


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
        if looks_like_image_id(image_id_or_slug):
            image = cls(token=api_token, id=image_id_or_slug)
            image.load()
        else:
            image = cls(token=api_token, slug=image_id_or_slug)
            image.load(use_slug=True)
        return image

    def load(self, use_slug=False):
        """
            Load slug.

            Loads by id, or by slug if id is not present or use slug is True.
        """
        identifier = None
        if use_slug or not self.id:
            identifier = self.slug
        else:
            identifier = self.id
        if not identifier:
            raise NotFoundError("One of self.id or self.slug must be set.")
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
