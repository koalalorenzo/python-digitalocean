# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT, NotFoundError


class Image(BaseAPI):
    """
    An object representing an DigitalOcean Image.

    Attributes accepted at creation time:

    Args:
        name (str): The name to be given to an image.
        url (str): A URL from which the virtual machine image may be retrieved.
        region (str): The slug of the region where the image will be available.
        distribution (str, optional): The name of the image's distribution.
        description (str, optional): Free-form text field to describe an image.
        tags (obj:`list` of `str`, optional): List of tag names to apply to
            the image.

    Attributes returned by API:

        id (int): A unique number to identify and reference a image.
        name (str): The display name given to an image.
        type (str): The kind of image. This will be either "snapshot",
            "backup", or "custom".
        distribution (str): The name of the image's distribution.
        slug (str): A uniquely identifying string that is associated with each
            of the DigitalOcean-provided public images.
        public (bool): Indicates whether the image is public or not.
        regions (obj:`list` of `str`): A list of the slugs of the regions where
            the image is available for use.
        created_at (str): A time value given in ISO8601 combined date and time
            format that represents when the image was created.
        min_disk_size (int): The minimum disk size in GB required for a Droplet
            to use this image.
        size_gigabytes (int): The size of the image in gigabytes.
        description (str): Free-form text field to describing an image.
        tags (obj:`list` of `str`): List of tag names to applied to the image.
        status (str): Indicates the state of a custom image. This may be "NEW",
            "available", "pending", or "deleted".
        error_message (str): Information about errors that may occur when
            importing a custom image.
    """
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
        self.description = None
        self.status = None
        self.tags = []
        self.error_message = None
        self.url = None
        self.region = None

        super(Image, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, image_id_or_slug):
        """
            Class method that will return an Image object by ID or slug.

            This method is used to validate the type of the image. If it is a
            number, it will be considered as an Image ID, instead if it is a
            string, it will considered as slug.
        """
        if cls._is_string(image_id_or_slug):
            image = cls(token=api_token, slug=image_id_or_slug)
            image.load(use_slug=True)
        else:
            image = cls(token=api_token, id=image_id_or_slug)
            image.load()
        return image

    @staticmethod
    def _is_string(value):
        """
            Checks if the value provided is a string (True) or not integer
            (False) or something else (None).
        """
        if type(value) in [type(u''), type('')]:
            return True
        elif type(value) in [int, type(2 ** 64)]:
            return False
        else:
            return None

    def create(self):
        """
        Creates a new custom DigitalOcean Image from the Linux virtual machine
        image located at the provided `url`.
        """
        params = {'name': self.name,
                  'region': self.region,
                  'url': self.url,
                  'distribution': self.distribution,
                  'description': self.description,
                  'tags': self.tags}

        data = self.get_data('images', type=POST, params=params)

        if data:
            for attr in data['image'].keys():
                setattr(self, attr, data['image'][attr])

        return self

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
