import digitalocean
from digitalocean.baseapi import BaseAPI


class Tag(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.name = ""
        self.resources = {}
        super(Tag, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, tag_name):
        tag = cls(token=api_token, name=tag_name)
        tag.load()
        return tag

    def load(self):
        """
           Fetch data about tag - use this instead of get_data()
        """
        tags = self.get_data("tags/%s" % self.name)
        tag = tags['tag']

        for attr in tag.keys():
            setattr(self, attr, tag[attr])

        return self

    def create(self, **kwargs):
        """
            Create the tag.
        """
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        data = {
            "name": self.name,
        }

        data = self.get_data("tags/", type="POST", params=data)
        if data:
            self.name = data['tag']['name']
            self.resources = data['tag']['resources']

    def load_or_create(self, **kwargs):
        """
            Load or create the tag.
        """
        create = False
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        try:
            self.load()
        except digitalocean.DataReadError:
            self.create()
            create = True
        return create

    def _resources(self, resources, type):
        if not resources:
            return True
        # TODO: check resources format
        # example: [{"resource_id": droplet.id, "resource_type": "droplet"}]
        tagged = self.get_data(
            'tags/%s/resources' % self.name, params={
                "resources": resources
            },
            type=type,
        )
        return tagged

    def tagging_resources(self, resources):
        return self._resources(resources, type='POST')

    def untagging_resources(self, resources):
        return self._resources(resources, type='DELETE')

    def tagging_droplets(self, droplet_ids):
        return self.tagging_resources([
           {"resource_id": droplet_id, "resource_type": "droplet"}
           for droplet_id in droplet_ids
        ])

    def untagging_droplets(self, droplet_ids):
        return self.untagging_resources([
           {"resource_id": droplet_id, "resource_type": "droplet"}
           for droplet_id in droplet_ids
        ])

    def tagging_droplet(self, droplet_id):
        return self.tagging_resources([{
            "resource_id": droplet_id,
            "resource_type": "droplet"
        }])

    def untagging_droplet(self, droplet_id):
        return self.untagging_resources([{
            "resource_id": droplet_id,
            "resource_type": "droplet"
        }])
