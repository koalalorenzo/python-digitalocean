from .baseapi import BaseAPI
import requests

class SSHKey(BaseAPI):
    id = ""
    name = None
    public_key = None
    fingerprint = None

    def __init__(self, token="", *args, **kwargs):
        super(SSHKey, self).__init__()
        if token:
            self.token = token

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def __call_api(self, type, params=dict()):
        headers = {'Authorization':'Bearer ' + self.token}
        if type == 'POST':
            headers['content-type'] = 'application/json'
            r = requests.post("https://api.digitalocean.com/v2/account/keys/",
                              headers=headers,
                              params=params)
        elif type == 'PUT':
            headers['content-type'] = 'application/json'
            r = requests.put("https://api.digitalocean.com/v2/account/keys/%s" %
                              self.id,
                              headers=headers,
                              params=params)
        elif type == 'DELETE':
            headers['content-type'] = 'application/x-www-form-urlencoded'
            r = requests.delete("https://api.digitalocean.com/v2/account/keys/%s" %
                              self.id,
                              headers=headers,
                              params=params)
        else:
            r = requests.get("https://api.digitalocean.com/v2/account/keys/%s" %
                             self.id,
                             headers=headers,
                             params=params)

        # A successful delete returns "204 No Content"
        if r.status_code != 204:
            data = r.json()
            self.call_response = data
            if r.status_code not in [requests.codes.ok, 202, 201]:
                msg = [data[m] for m in ("id", "message") if m in data][1]
                raise Exception(msg)

            return data

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
