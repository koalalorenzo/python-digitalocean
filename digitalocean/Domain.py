# -*- coding: utf-8 -*-
from .Record import Record
from .baseapi import BaseAPI, GET, POST, DELETE, PUT


class Domain(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.name = None
        self.ttl = None
        self.zone_file = None
        self.ip_address = None

        super(Domain, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, domain_name):
        """
            Class method that will return a Domain object by ID.
        """
        domain = cls(token=api_token, name=domain_name)
        domain.load()
        return domain

    def load(self):
        # URL https://api.digitalocean.com/v2/domains
        domains = self.get_data("domains/%s" % self.name)
        domain = domains['domain']

        for attr in domain.keys():
            setattr(self, attr, domain[attr])

    def destroy(self):
        """
            Destroy the domain by name
        """
        # URL https://api.digitalocean.com/v2/domains/[NAME]
        return self.get_data("domains/%s" % self.name, type=DELETE)

    def create_new_domain_record(self, *args, **kwargs):
        """
            Create new domain record.
            https://developers.digitalocean.com/#create-a-new-domain-record

            Args:
                type: The record type (A, MX, CNAME, etc).
                name: The host name, alias, or service being defined by the record
                data: Variable data depending on record type.

            Optional Args:
                priority: The priority of the host
                port: The port that the service is accessible on
                weight: The weight of records with the same priority
                ttl: This value is the time to live for the record, in seconds.
                flags: An unsigned integer between 0-255 used for CAA records.
                tag: The parameter tag for CAA records. Valid values are "issue",
                    "issuewild", or "iodef".
        """
        data = {
            "type": kwargs.get("type", None),
            "name": kwargs.get("name", None),
            "data": kwargs.get("data", None)
        }

        #  Optional Args
        if kwargs.get("priority", None) != None:
            data['priority'] = kwargs.get("priority", None)

        if kwargs.get("port", None):
            data['port'] = kwargs.get("port", None)

        if kwargs.get("weight", None) != None:
            data['weight'] = kwargs.get("weight", None)

        if kwargs.get("ttl", None):
            data['ttl'] = kwargs.get("ttl", 1800)

        if kwargs.get("flags", None) != None:
            data['flags'] = kwargs.get("flags", None)

        if kwargs.get("tag", None):
            data['tag'] = kwargs.get("tag", "issue")

        if self.ttl:
            data['ttl'] = self.ttl

        return self.get_data(
            "domains/%s/records" % self.name,
            type=POST,
            params=data
        )

    def update_domain_record(self, *args, **kwargs):
        """
            Args:
                type: The record type (A, MX, CNAME, etc).
                name: The host name, alias, or service being defined by the record
                data: Variable data depending on record type.
                priority: The priority of the host
                port: The port that the service is accessible on
                weight: The weight of records with the same priority
        """
        data = {
            'id': kwargs.get("id", None),
            'domain': kwargs.get("domain", None)
        }

        if kwargs.get("data", None):
            data['data'] = kwargs.get("data", None)

        if kwargs.get("type", None):
            data['type'] = kwargs.get("type", None)

        if kwargs.get("name", None):
            data['name'] = kwargs.get("name", None)

        if kwargs.get("port", None):
            data['port'] = kwargs.get("port", None)

        if kwargs.get("weight", None):
            data['weight'] = kwargs.get("weight", None)

        return self.get_data(
            "domains/%s/records/%s" % (data['domain'], data['id']),
            type=PUT,
            params=data
        )

    def delete_domain_record(self, *args, **kwargs):

        data = {
            'id': kwargs.get("id", None)
        }

        return self.get_data(
            "domains/%s/records/%s" % (self.name, data['id']),
            type=DELETE
        )

    def create(self):
        """
            Create new domain
        """
        # URL https://api.digitalocean.com/v2/domains
        data = {
            "name": self.name,
            "ip_address": self.ip_address,
        }

        domain = self.get_data("domains", type=POST, params=data)
        return domain

    def get_records(self, params=None):
        """
            Returns a list of Record objects
        """
        if params is None:
            params = {}
        
        # URL https://api.digitalocean.com/v2/domains/[NAME]/records/
        records = []
        data = self.get_data("domains/%s/records/" % self.name, type=GET, params=params)

        for record_data in data['domain_records']:

            record = Record(domain_name=self.name, **record_data)
            record.token = self.token
            records.append(record)

        return records

    def __str__(self):
        return "%s" % (self.name)
