import requests
from .baseapi import BaseAPI

class Image(BaseAPI):
    id = None
    name = None
    distribution = None
    slug = None
    public = None
    regions = []
    created_at = None

    def __init__(self, token=""):
        super(Image, self).__init__()
        if token:
            self.token = token

    def __call_api(self, type, path, params=dict()):
        payload = {}
        headers = {'Authorization':'Bearer ' + self.token}
        payload.update(params)
        if type == 'POST':
            headers['content-type'] = 'application/json'
            r = requests.post("https://api.digitalocean.com/v2/images/%s%s" %
                             (self.id, path),
                              headers=headers,
                              params=payload)
        elif type == 'PUT':
            headers['content-type'] = 'application/json'
            r = requests.put("https://api.digitalocean.com/v2/images/%s%s" %
                             (self.id, path),
                              headers=headers,
                              params=payload)
        elif type == 'DELETE':
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
        return self.get_data(
            "images/%s/destroy/" % self.id,
            type="DELETE",
        )

    def transfer(self, new_region_slug):
        """
            Transfer the image
        """
        return self.get_data(
            "images/%s/actions/" % self.id,
            type="POST",
            params={"type": "transfer", "region": new_region_slug}
        )

    def rename(self, new_name):
        """
            Rename an image
        """
        return self.get_data(
            "images/%s" % self.id,
            type="PUT",
            params={"name": new_name}
        )
