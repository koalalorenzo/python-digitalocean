# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT


class CDNEndpoint(BaseAPI):
    """
    An object representing an DigitalOcean CDN Endpoint.

    Args:
        origin (str): The fully qualified domain name (FQDN) for the
            origin server which provides the content for the CDN.
            This is currently restricted to a Space.
        ttl (int): The amount of time the content is cached by the
            CDN's edge servers in seconds. TTL must be one of
            60, 600, 3600, 86400, or 604800.
            Defaults to 3600 (one hour) when excluded.
        certificate_id (str): The ID of a DigitalOcean managed TLS
            certificate used for SSL when a custom subdomain is provided.
        custom_domain (str): The fully qualified domain name (FQDN) of the
            custom subdomain used with the CDN endpoint.
    """

    def __init__(self, *args, **kwargs):
        self.id = None
        self.origin = None
        self.endpoint = None
        self.created_at = None
        self.certificate_id = None
        self.custom_domain = None
        self.ttl = None

        super(CDNEndpoint, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, cdn_endpoint_id):
        """Class method that will return a CDN Endpoint object by ID.

        Args:
            api_token (str): token
            cdn_endpoint_id (int): CDN Endpoint id
        """
        cdn_endpoint = cls(token=api_token, id=cdn_endpoint_id)
        cdn_endpoint.load()
        return cdn_endpoint

    def load(self):
        """
           Fetch data about CDN Endpoints - use this instead of get_data()
        """
        cdn_endpoints = self.get_data("cdn/endpoints/%s" % self.id)
        cdn_endpoint = cdn_endpoints['endpoint']

        for attr in cdn_endpoint.keys():
            setattr(self, attr, cdn_endpoint[attr])

        return self

    def create(self, **kwargs):
        """
            Create the CDN Endpoint.
        """
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        params = {
            'origin': self.origin,
            'ttl': self.ttl or 3600,
            'certificated_id': self.certificate_id,
            'custom_domain': self.custom_domain
        }

        output = self.get_data("cdn/endpoints", type="POST", params=params)
        if output:
            self.id = output['endpoint']['id']
            self.created_at = output['endpoint']['created_at']
            self.endpoint = output['endpoint']['endpoint']


    def delete(self):
        """
            Delete the CDN Endpoint.
        """
        return self.get_data("cdn/endpoints/%s" % self.id, type="DELETE", params=False)

    def save(self):
        """
            Save existing CDN Endpoint
        """
        data = {
            'ttl': self.ttl,
            'certificate_id': self.certificate_id,
            'custom_domain': self.custom_domain,
        }
        return self.get_data(
            "cdn/endpoints/%s" % self.id,
            type=PUT,
            params=data
        )


    def __str__(self):
        return "<CDNEndpoints: %s %s>" % (self.id, self.origin)
