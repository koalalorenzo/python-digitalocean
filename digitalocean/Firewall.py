# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT


class Firewall(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.status = None
        self.created_at = None
        self.pending_changes = []
        self.name = None
        self.inbound_rules = None
        self.outbound_rules = None
        self.droplet_ids = None
        self.tags = None

        super(Firewall, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, firewall_id):
        """
            Class method that will return a Firewall object by ID.
        """
        firewall = cls(token=api_token, id=firewall_id)
        firewall.load()
        return firewall

    def load(self):
        data = self.get_data("firewalls/%s" % self.id)
        firewall_dict = data['firewall']

        # Setting the attribute values
        for attr in firewall_dict.keys():
            setattr(self, attr, firewall_dict[attr])

        return self

    def add_droplets(self, droplet_ids):
        """
            Add droplets to this Firewall.
        """
        return self.get_data(
            "firewalls/%s/droplets" % self.id,
            type=POST,
            params={"droplet_ids": droplet_ids}
        )

    def remove_droplets(self, droplet_ids):
        """
            Remove droplets from this Firewall.
        """
        return self.get_data(
            "firewalls/%s/droplets" % self.id,
            type=DELETE,
            params={"droplet_ids": droplet_ids}
        )

    def add_tags(self, tags):
        """
            Add tags to this Firewall.
        """
        return self.get_data(
            "firewalls/%s/tags" % self.id,
            type=POST,
            params={"tags": tags}
        )

    def remove_tags(self, tags):
        """
            Remove tags from this Firewall.
        """
        return self.get_data(
            "firewalls/%s/tags" % self.id,
            type=DELETE,
            params={"tags": tags}
        )

    # TODO: Other Firewall calls (Add/Remove rules, Create / Delete etc)

    def destroy(self):
        """
            Destroy the Firewall
        """
        return self.get_data("firewalls/%s/" % self.id, type=DELETE)

    def __str__(self):
        return "<Firewall: %s %s>" % (self.id, self.name)
