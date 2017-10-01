# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT


class _targets(object):
    """
    """
    def __init__(self, addresses=[], droplet_ids=[],
                 load_balancer_uids=[], tags=[]):
        self.addresses = addresses
        self.droplet_ids = droplet_ids
        self.load_balancer_uids = load_balancer_uids
        self.tags = tags


class Sources(_targets):
    pass


class Destinations(_targets):
    pass


class InboundRule(object):
    """
    """
    def __init__(self, protocol=None, ports=None, sources=[]):
        self.protocol = protocol
        self.ports = ports
        self.sources = []

        for source in sources:
            self.sources.append(Sources(**sources))


class OutboundRule(object):
    """
    """
    def __init__(self, protocol=None, ports=None, destinations=[]):
        self.protocol = protocol
        self.ports = ports
        self.destinations = []

        for destination in destinations:
            self.destinations.append(Destinations(**destinations))


class Firewall(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.status = None
        self.created_at = None
        self.pending_changes = []
        self.name = None
        self.inbound_rules = []
        self.outbound_rules = []
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
            if attr == 'inbound_rules':
                rules = list()
                for rule in firewall_dict['inbound_rules']:
                    rules.append(InboundRule(**rule))
                setattr(self, attr, rules)
            elif attr == 'outbound_rules':
                rules = list()
                for rule in firewall_dict['outbound_rules']:
                    rules.append(OutboundRule(**rule))
                setattr(self, attr, rules)
            else:
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
