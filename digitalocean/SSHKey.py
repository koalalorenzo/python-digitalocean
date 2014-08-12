from .baseapi import BaseAPI
import requests

class SSHKey(BaseAPI):
    id = ""
    name = None
    public_key = None
    fingerprint = None

    def __init__(self, *args, **kwargs):
        super(SSHKey, self).__init__()

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def load(self):
        data = self.get_data(
            "account/keys/%s" % self.id,
            type="GET"
        )

        ssh_key = data['ssh_key']

        self.public_key = ssh_key['public_key']
        self.name = ssh_key['name']
        self.id = ssh_key['id']
        self.fingerprint = ssh_key['fingerprint']

    def create(self):
        """
            Create the SSH Key
        """
        input_params = {
                "name": self.name,
                "public_key": self.public_key,
            }

        data = self.get_data(
            "account/keys/",
            type="POST",
            params=input_params
        )

        if data:
            self.id = data['ssh_key']['id']

    def edit(self):
        """
            Edit the SSH Key
        """
        input_params = {
                "name": self.name,
                "public_key": self.public_key,
            }

        data = self.get_data(
            "account/keys/%s" % self.id,
            type="PUT",
            params=input_params
        )

        if data:
            self.id = data['ssh_key']['id']

    def destroy(self):
        """
            Destroy the SSH Key
        """
        return self.get_data(
            "account/keys/%s" % self.id,
            type="DELETE",
        )
