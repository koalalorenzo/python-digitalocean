# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE


class Certificate(BaseAPI):
    """
    An object representing an SSL Certificate stored on DigitalOcean.

    Attributes accepted at creation time:

    Args:
        name (str): A name for the Certificate
        private_key (str, optional): The contents of a PEM-formatted
            private-key corresponding to the SSL certificate. Only used
            when uploading a custom certificate.
        leaf_certificate (str, optional): The contents of a PEM-formatted
            public SSL certificate. Only used when uploading a custom
            certificate.
        certificate_chain (str, optional): The full PEM-formatted trust chain
            between the certificate authority's certificate and your domain's
            SSL certificate. Only used when uploading a custom certificate.
        dns_names (:obj:`str`): A list of fully qualified domain names (FQDNs)
            for which the certificate will be issued by Let's Encrypt
        type (str): Specifies the type of certificate to be created. The value
            should be "custom" for a user-uploaded certificate or
            "lets_encrypt" for one automatically generated with Let's Encrypt.

    Attributes returned by API:
        name (str): The name of the Certificate
        id (str): A unique identifier for the Certificate
        not_after (str): A string that represents the Certificate's expiration
            date.
        sha1_fingerprint (str): A unique identifier for the Certificate
            generated from its SHA-1 fingerprint
        created_at (str): A string that represents when the Certificate was
            created
        dns_names (:obj:`str`): A list of fully qualified domain names (FQDNs)
            for which a Let's Encrypt generated certificate is issued.
        type (str): Specifies the type of certificate. The value will be
            "custom" for a user-uploaded certificate or "lets_encrypt" for one
            automatically generated with Let's Encrypt.
        state (str): Represents the current state of the certificate. It may be
            "pending", "verified", or "errored".
    """
    def __init__(self, *args, **kwargs):
        self.id = ""
        self.name = None
        self.private_key = None
        self.leaf_certificate = None
        self.certificate_chain = None
        self.not_after = None
        self.sha1_fingerprint = None
        self.created_at = None
        self.dns_names = []
        self.type = None
        self.state = None

        super(Certificate, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, cert_id):
        """
            Class method that will return a Certificate object by its ID.
        """
        certificate = cls(token=api_token, id=cert_id)
        certificate.load()
        return certificate

    def load(self):
        """
            Load the Certificate object from DigitalOcean.

            Requires self.id to be set.
        """
        data = self.get_data("certificates/%s" % self.id)
        certificate = data["certificate"]

        for attr in certificate.keys():
            setattr(self, attr, certificate[attr])

        return self

    def create(self):
        """
            Create the Certificate
        """
        params = {
            "name": self.name,
            "type": self.type,
            "dns_names": self.dns_names,
            "private_key": self.private_key,
            "leaf_certificate": self.leaf_certificate,
            "certificate_chain": self.certificate_chain
        }

        data = self.get_data("certificates", type=POST, params=params)

        if data:
            self.id = data['certificate']['id']
            self.not_after = data['certificate']['not_after']
            self.sha1_fingerprint = data['certificate']['sha1_fingerprint']
            self.created_at = data['certificate']['created_at']
            self.type = data['certificate']['type']
            self.dns_names = data['certificate']['dns_names']
            self.state = data['certificate']['state']

        return self

    def destroy(self):
        """
            Delete the Certificate
        """
        return self.get_data("certificates/%s" % self.id, type=DELETE)

    def __str__(self):
        return "<Certificate: %s %s>" % (self.id, self.name)
