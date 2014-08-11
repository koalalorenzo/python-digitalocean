import requests
from .baseapi import BaseAPI

class Record(BaseAPI):
    domain = ""
    id = None
    type = None
    name = None
    data = None
    priority = None
    port = None
    weight = None

    def __init__(self, domain_name, id="", token=""):
        super(Record, self).__init__()
        self.domain = domain_name
        if id:
            self.id = id
        if token:
            self.token = token

    def __call_api(self, type, path, params=dict()):
        headers = {'Authorization':'Bearer ' + self.token}
        if type == 'POST':
            headers['content-type'] = 'application/json'
            r = requests.post("https://api.digitalocean.com/v2/domains/%s/records/%s%s" % (
                              self.domain, self.id, path),
                              headers=headers,
                              params=params)
        elif type == 'PUT':
            headers['content-type'] = 'application/json'
            r = requests.put("https://api.digitalocean.com/v2/domains/%s/records/%s%s" % (
                              self.domain, self.id, path),
                              headers=headers,
                              params=params)
        elif type == 'DELETE':
            headers['content-type'] = 'application/x-www-form-urlencoded'
            r = requests.delete("https://api.digitalocean.com/v2/domains/%s/records/%s%s" % (
                              self.domain, self.id, path),
                              headers=headers,
                              params=params)
        else:
            r = requests.get("https://api.digitalocean.com/v2/domains/%s/records/%s%s" % (
                             self.domain, self.id, path),
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

    def create(self):
        """
            Create a record for a domain
        """
        input_params = {
                "type": self.type,
                "data": self.data,
                "name": self.name,
                "priority": self.priority,
                "port": self.port,
                "weight": self.weight
            }

        data = self.get_data(
            "domains/%s/records/%s" % (self.domain, self.id),
            type="POST",
            params=input_params,
        )

        if data:
            self.id = data['domain_record']['id']

    def destroy(self):
        """
            Destroy the record
        """
        return self.get_data(
            "domains/%s/records/%s" % (self.domain, self.id),
            type="DELETE",
        )

    def save(self):
        """
            Save existing record
        """
        data = {
            "type": self.type,
            "data": self.data,
            "name": self.name,
            "priority": self.priority,
            "port": self.port,
            "weight": self.weight,
        }
        return self.get_data(
            "domains/%s/records/%s" % (self.domain, self.id),
            type="PUT",
            params=data
        )

    def load(self):
        url = "domains/%s/records/%s" % (self.domain, self.id)
        record = self.get_data(url)
        if record:
            record = record[u'domain_record']
            self.id = record['id']
            self.type = record[u'type']
            self.name = record[u'name']
            self.data = record[u'data']
            self.priority = record[u'priority']
            self.port = record[u'port']
            self.weight = record[u'weight']