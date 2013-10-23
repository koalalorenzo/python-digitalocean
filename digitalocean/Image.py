import requests

class Image(object):
    def __init__(self, client_id="", api_key=""):
        self.client_id = client_id
        self.api_key = api_key

        self.name = None
        self.id = None
        self.distribution = None

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/images/%s%s" % ( self.id, path ), params=payload)
        data = r.json()
        self.call_response = data
        if data['status'] != "OK":
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
            raise Exception(msg)

        return data

    def Destroy(self):
        """
            Destroy the image
        """
        self.__call_api("/destroy/")

    def transfer(self, new_region_id):
        """
            Transfer the image
        """
        self.__call_api("/transfer/", {"region_id": new_region_id})
