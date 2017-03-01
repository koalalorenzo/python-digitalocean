# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE


class Certificate(BaseAPI):
    """
    {
  "certificate": {
    "id": "892071a0-bb95-49bc-8021-3afd67a210bf",
    "name": "web-cert-01",
    "not_after": "2017-02-22T00:23:00Z",
    "sha1_fingerprint": "dfcc9f57d86bf58e321c2c6c31c7a971be244ac7",
    "created_at": "2017-02-08T16:02:37Z"
  }
}
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

        super(Certificate, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, cert_id):
        """
            Class method that will return a Certificate object by ID.
        """
        certificate = cls(token=api_token, id=cert_id)
        certificate.load()
        return certificate

    def load(self):
        """
            Load the Certificate object from DigitalOcean.

            Requires either self.id to be set.
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
            "private_key": self.private_key,
            "leaf_certificate": self.leaf_certificate,
            "certificate_chain": self.certificate_chain
        }

        data = self.get_data("certificates/", type=POST, params=params)

        if data:
            self.id = data['certificate']['id']
            self.not_after = data['certificate']['not_after']
            self.sha1_fingerprint = data['certificate']['sha1_fingerprint']
            self.created_at = data['certificate']['created_at']

    def destroy(self):
        """
            Delete the Certificate
        """
        return self.get_data("certificates/%s" % self.id, type=DELETE)

    def __str__(self):
        return "<Certificate: %s %s>" % (self.id, self.name)
