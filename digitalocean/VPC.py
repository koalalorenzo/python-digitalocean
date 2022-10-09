# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, PATCH, POST, DELETE


class VPC(BaseAPI):
    """
    An object representing a DigitalOcean VPC.

    Attributes accepted at creation time:

    Args:
        name (str): A name for the VPC
        region (str): The slug for the region where the VPC will be created
        description(str): A free-form text field for describing the VPC
        ip_range (str): The requested range of IP addresses for the VPC in \
            CIDR notation


    Attributes returned by API:
        * id (str): A unique identifier for the VPC
        * name (str): The name of the VPC
        * region (str): The slug for the region where the VPC is located
        * description(str): A free-form text field for describing the VPC
        * ip_range (str): The requested range of IP addresses for the VPC in \
            CIDR notation
        * urn (str): The uniform resource name (URN) for the VPC
        * created_at (str): A string that represents when the VPC was created
        * default (bool): A boolean representing whether or not the VPC is the \
            user's default VPC for the region
    """
    def __init__(self, *args, **kwargs):
        self.id = ""
        self.name = None
        self.region = None
        self.description = None
        self.ip_range = None
        self.urn = None
        self.created_at = None
        self.default = False

        super(VPC, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, vpc_id):
        """
            Class method that will return a VPC object by its ID.
        """
        vpc = cls(token=api_token, id=vpc_id)
        vpc.load()
        return vpc

    def load(self):
        """
            Load the VPC object from DigitalOcean.

            Requires self.id to be set.
        """
        data = self.get_data("vpcs/%s" % self.id)
        vpc = data["vpc"]

        for attr in vpc.keys():
            setattr(self, attr, vpc[attr])

        return self

    def create(self):
        """
            Create the VPC
        """
        params = {
            "name": self.name,
            "region": self.region,
            "description": self.description,
            "ip_range": self.ip_range
        }

        data = self.get_data("vpcs", type=POST, params=params)

        if data:
            self.id = data['vpc']['id']
            self.name = data['vpc']['name']
            self.region = data['vpc']['region']
            self.description = data['vpc']['description']
            self.ip_range = data['vpc']['ip_range']
            self.urn = data['vpc']['urn']
            self.created_at = data['vpc']['created_at']
            self.default = data['vpc']['default']

        return self

    def rename(self, new_name):
        """
            Rename a VPC

            Args:
                name (str): The new name for the VPC
        """
        data = self.get_data("vpcs/%s" % self.id,
                             type=PATCH,
                             params={"name": new_name})

        vpc = data["vpc"]

        for attr in vpc.keys():
            setattr(self, attr, vpc[attr])

        return self

    def rename(self, new_name):
        """
            Rename a VPC

            Args:
                name (str): The new name for the VPC
        """
        data = self.get_data("vpcs/%s" % self.id,
                             type=PATCH,
                             params={"name": new_name})

        vpc = data["vpc"]

        for attr in vpc.keys():
            setattr(self, attr, vpc[attr])

        return self

    def destroy(self):
        """
            Delete the VPC
        """
        return self.get_data("vpcs/%s" % self.id, type=DELETE)

    def __str__(self):
        return "<VPC: %s %s>" % (self.id, self.name)
