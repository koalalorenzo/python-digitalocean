import requests

class SSHKey(object):
    def __init__(self, token="", *args, **kwargs):

        self.token = token

        self.id = ""
        self.name = None
        self.public_key = None
        self.fingerprint = None

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
        ssh_key = self.__call_api("GET")['ssh_key']
        self.public_key = ssh_key['public_key']
        self.name = ssh_key['name']
        self.id = ssh_key['id']
        self.fingerprint = ssh_key['fingerprint']

    def create(self):
        """
            Create the SSH Key
        """
        data = {
                "name": self.name,
                "public_key": self.public_key,
            }
        data = self.__call_api("POST", data)
        if data:
            self.id = data['ssh_key']['id']

    def edit(self):
        """
            Edit the SSH Key
        """
        data = {
                "name": self.name,
                "public_key": self.public_key,
            }
        data = self.__call_api("PUT", data)
        if data:
            self.id = data['ssh_key']['id']

    def destroy(self):
        """
            Destroy the SSH Key
        """
        self.__call_api("DELETE")
