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