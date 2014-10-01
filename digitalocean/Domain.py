import requests
from .Record import Record
from .baseapi import BaseAPI

class Domain(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.name = None
        self.ttl = None
        self.zone_file = None
        self.ip_address = None

        super(Domain, self).__init__(*args, **kwargs)

    def load(self):
        # URL https://api.digitalocean.com/v2/domains
        domains = self.get_data("domains/%s" % self.name)
        domain = domains[u'domain']
        self.zone_file = domain[u'zone_file']
        self.ttl = domain[u'ttl']
        self.name = domain[u'name']

    def destroy(self):
        """
            Destroy the domain by name
        """
        # URL https://api.digitalocean.com/v2/domains/[NAME]
        return self.get_data(
            "domains/%s" % self.name,
            type="DELETE"
        )

    def create_new_domain_record(self, *args, **kwargs):
        data = {
            "type": kwargs.get("type" None),
            "name": kwargs.get("name" None),
            "data": kwargs.get("data" None)
        }

        # Optional Args
        if kwargs.get("priority", None):
            data['priority'] = kwargs.get("priority", None)

        if kwargs.get("port", None):
            data['port'] = kwargs.get("port", None)

        if kwargs.get("weight", None):
            data['weight'] = kwargs.get("weight", None)

        return self.get_data(
            "domains/%s/records" % self.name,
            type="POST",
            params=data
        )

    def create(self):
        """
            Create new doamin
        """
        # URL https://api.digitalocean.com/v2/domains
        data = {
                "name": self.name,
                "ip_address": self.ip_address,
            }

        domain = self.get_data(
            "domains",
            type="POST",
            params=data
        )
        return domain

    def get_records(self):
        """
            Returns a list of Record objects
        """
        # URL https://api.digitalocean.com/v2/domains/[NAME]/records/
        records = []
        data = self.get_data(
            "domains/%s/records/" % self.name,
            type="GET",
            params=data
        )

        for record_data in data['domain_records']:

            record = Record(**record_data)
            record.token = self.token
            records.append(record)

        return records

    def __str__(self):
        return "%s" % self.name