import requests
from .baseapi import BaseAPI

class Record(BaseAPI):
    def __init__(self, domain_name, *args, **kwargs):
        self.domain = domain_name if domain_name else ""
        self.id = None
        self.type = None
        self.name = None
        self.data = None
        self.priority = None
        self.port = None
        self.weight = None

        super(Record, self).__init__(*args, **kwargs)

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

            #Setting the attribute values
            for attr in record.keys():
                setattr(self,attr,record[attr])
