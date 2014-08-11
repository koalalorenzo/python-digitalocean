import requests
from .Record import Record
from .baseapi import BaseAPI

class Domain(BaseAPI):
    name = None
    ttl = None
    zone_file = None
    ip_address = None

    def __init__(self, *args, **kwargs):
        super(Domain, self).__init__()
        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def load(self):
        # URL https://api.digitalocean.com/v2/domains
        domains = self.get_data("domains")
        domain = domains['domain']
        self.live_zone_file = domain['zone_file']
        self.ttl = domain['ttl']
        self.name = domain['name']

    def destroy(self):
        """
            Destroy the domain by name
        """
        # URL https://api.digitalocean.com/v2/domains/[NAME]
        domain = self.get_data(
            "domains/%s" % self.name,
            type="DELETE"
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
            "domains/%s/records/" % self.name,,
            type="GET",
            params=data
        )

        for record_data in data['domain_records']:
            record = Record(domain_name=self.name,
                            id=record_data.pop('id'))
            for key, value in record_data.iteritems():
                setattr(record, key, value)
            record.token = self.token
            records.append(record)
        return records
