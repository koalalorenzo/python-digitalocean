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


    def __build_resources(self, data, object_class, resource_type):
        """
            Private method to build the `resources` field used to tag/untag 
            objects.
            It will check the type of object in the array provided and build
            the right structure for the API.
            The 2nd and 3rd arguments specify the object class and the latter 
            takes the resource type as required by DO API.
        """
        resources = []
        if not isinstance(data, list): return data
        for obj in data:
            res = {}

            try:
                if isinstance(obj, unicode):
                    res = {"resource_id": obj}
            except NameError:
                pass

            if isinstance(obj, str) or isinstance(obj, int):
                res = {"resource_id": str(obj)}
            elif isinstance(obj, object_class):
                res = {"resource_id": str(obj.id)}

            if len(res) > 0:
                res["resource_type"] = resource_type
                resources.append(res)

        return resources


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
        resources = self.__build_resources(droplets, Droplet, "droplet")
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
        resources = self.__build_resources(droplets, Droplet, "droplet")
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

        resources = self.__build_resources(snapshots, Snapshot, "volume_snapshot")
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

        resources = self.__build_resources(snapshots, Snapshot, "volume_snapshot")
        if len(resources) > 0:
            return self.__remove_resources(resources)
        
        return False

