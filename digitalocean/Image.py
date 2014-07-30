import requests

class Image(object):
    def __init__(self, token=""):
        self.token = token
        self.id = None
        self.name = None
        self.distribution = None
        self.slug = None
        self.public = None
        self.regions = []
        self.created_at = None

    def __call_api(self, type, path, params=dict()):
        payload = {'token': self.token}
        headers = {'Authorization':'Bearer ' + self.token}
        payload.update(params)
        if type == 'PUT':
            headers['content-type'] = 'application/json'
            r = requests.post("https://api.digitalocean.com/v2/images/%s%s" %
                             (self.id, path),
                              headers=headers,
                              params=payload)
        if type == 'DELETE':
            headers['content-type'] = 'application/x-www-form-urlencoded'
            r = requests.delete("https://api.digitalocean.com/v2/images/%s" %
                             (self.id),
                              headers=headers,
                              params=payload)

        # A successful delete returns "204 No Content"
        if r.status_code != 204:
            data = r.json()
            self.call_response = data
            if r.status_code != requests.codes.ok:
                msg = [data[m] for m in ("id", "message") if m in data][1]
                raise Exception(msg)

            return data

    def destroy(self):
        """
            Destroy the image
        """
        self.__call_api("DELETE", "/destroy/")

    def transfer(self, new_region_slug):
        """
            Transfer the image
        """
        self.__call_api("PUT", "/actions/",
                       {"type": "transfer", "region": new_region_slug})
