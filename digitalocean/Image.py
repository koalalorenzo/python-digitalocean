import requests
from .baseapi import BaseAPI

class Image(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.name = None
        self.distribution = None
        self.slug = None
        self.public = None
        self.regions = []
        self.created_at = None

        super(Image, self).__init__(*args, **kwargs)

    def destroy(self):
        """
            Destroy the image
        """
        return self.get_data(
            "images/%s/destroy/" % self.id,
            type="DELETE",
        )

    def transfer(self, new_region_slug):
        """
            Transfer the image
        """
        return self.get_data(
            "images/%s/actions/" % self.id,
            type="POST",
            params={"type": "transfer", "region": new_region_slug}
        )

    def rename(self, new_name):
        """
            Rename an image
        """
        return self.get_data(
            "images/%s" % self.id,
            type="PUT",
            params={"name": new_name}
        )

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.distribution)