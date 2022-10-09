from .baseapi import BaseAPI
from .Droplet import Droplet
from .Snapshot import Snapshot

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
           Fetch data about tag
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

        params = {"name": self.name}

        output = self.get_data("tags", type="POST", params=params)
        if output:
            self.name = output['tag']['name']
            self.resources = output['tag']['resources']


    def delete(self):
        return self.get_data("tags/%s" % self.name, type="DELETE")


    def __get_resources(self, resources, method):

        """ Method used to talk directly to the API (TAGs' Resources) """
        tagged = self.get_data(
            'tags/%s/resources' % self.name, params={
                "resources": resources
            },
            type=method,
        )
        return tagged


    def __add_resources(self, resources):
        """
            Add the resources to this tag.

            Attributes accepted at creation time:
                resources: array - See API.
        """
        return self.__get_resources(resources, method='POST')


    def __remove_resources(self, resources):
        """
            Remove resources from this tag.

            Attributes accepted at creation time:
                resources: array - See API.
        """
        return self.__get_resources(resources, method='DELETE')


    def __build_resources_field(self, resources_to_tag, object_class, resource_type):
        """
            Private method to build the `resources` field used to tag/untag 
            DO resources. Returns an array of objects containing two fields: 
            resource_id and resource_type.
            It checks the type of objects in the 1st argument and build the
            right structure for the API. It accepts array of strings, array
            of ints and array of the object type defined by object_class arg.
            The 3rd argument specify the resource type as defined by DO API
            (like droplet, image, volume or volume_snapshot).
            See: https://developers.digitalocean.com/documentation/v2/#tag-a-resource
        """
        resources_field = []
        if not isinstance(resources_to_tag, list): return resources_to_tag
        for resource_to_tag in resources_to_tag:
            res = {}

            try:
                if isinstance(resource_to_tag, unicode):
                    res = {"resource_id": resource_to_tag}
            except NameError:
                pass

            if isinstance(resource_to_tag, str) or isinstance(resource_to_tag, int):
                res = {"resource_id": str(resource_to_tag)}
            elif isinstance(resource_to_tag, object_class):
                res = {"resource_id": str(resource_to_tag.id)}

            if len(res) > 0:
                res["resource_type"] = resource_type
                resources_field.append(res)

        return resources_field


    def add_droplets(self, droplet):
        """
            Add the Tag to a Droplet.

            Attributes accepted at creation time:
                droplet: array of string or array of int, or array of Droplets.
        """
        droplets = droplet
        if not isinstance(droplets, list):
            droplets = [droplet]

        # Extracting data from the Droplet object
        resources = self.__build_resources_field(droplets, Droplet, "droplet")
        if len(resources) > 0:
            return self.__add_resources(resources)

        return False


    def remove_droplets(self, droplet):
        """
            Remove the Tag from the Droplet.

            Attributes accepted at creation time:
                droplet: array of string or array of int, or array of Droplets.
        """
        droplets = droplet
        if not isinstance(droplets, list):
            droplets = [droplet]

        # Build resources field from the Droplet objects
        resources = self.__build_resources_field(droplets, Droplet, "droplet")
        if len(resources) > 0:
            return self.__remove_resources(resources)

        return False


    def add_snapshots(self, snapshots):
        """
            Add the Tag to the Snapshot.

            Attributes accepted at creation time:
                snapshots: array of string or array of int or array of Snapshot.
        """
        
        if not isinstance(snapshots, list):
            snapshots = [snapshots]

        resources = self.__build_resources_field(snapshots, Snapshot, "volume_snapshot")
        if len(resources) > 0:
            return self.__add_resources(resources)
        
        return False


    def remove_snapshots(self, snapshots):
        """
            remove the Tag from the Snapshot.

            Attributes accepted at creation time:
                snapshots: array of string or array of int or array of Snapshot.
        """
        if not isinstance(snapshots, list):
            snapshots = [snapshots]

        resources = self.__build_resources_field(snapshots, Snapshot, "volume_snapshot")
        if len(resources) > 0:
            return self.__remove_resources(resources)
        
        return False


    def __str__(self):
        return "<Tag: %s>" % self.name

