import requests

class SSHKey(object):
    def __init__(self, client_id="", api_key="", *args, **kwargs):

        self.client_id = client_id
        self.api_key = api_key

        self.id = ""
        self.name = None
        self.ssh_pub_key = None

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/ssh_keys/%s%s" % ( self.id, path ), params=payload)

        data = r.json()
        self.call_response = data
        if data['status'] != "OK":
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
            raise Exception(msg)

        return data

    def load(self):
        ssh_key = self.__call_api("")['ssh_key']
        self.ssh_pub_key = ssh_key['ssh_pub_key']
        self.name = ssh_key['name']
        self.id = ssh_key['id']

    def create(self):
        """
            Create the SSH Key
        """
        data = {
                "name": self.name,
                "ssh_pub_key": self.ssh_pub_key,
            }
        data = self.__call_api("/new/", data)
        if data:
            self.id = data['ssh_key']['id']

    def edit(self):
        """
            Edit the SSH Key
        """
        data = {
                "name": self.name,
                "ssh_pub_key": self.ssh_pub_key,
            }
        data = self.__call_api("/edit/", data)
        if data:
            self.id = data['ssh_key']['id']

    def destroy(self):
        """
            Destroy the SSH Key
        """
        self.__call_api("/destroy/")
