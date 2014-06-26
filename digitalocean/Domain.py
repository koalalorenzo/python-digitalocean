import requests
from .Record import Record

class Domain(object):
    def __init__(self, *args, **kwargs):
        self.id = ""
        self.client_id = ""
        self.api_key = ""
        self.name = None
        self.ttl = None
        self.live_zone_file = None
        self.error = None
        self.zone_file_with_error = None
        self.records = []

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/v1/domains/%s%s" % ( self.id, path ), params=payload)
        data = r.json()
        self.call_response = data
        if data['status'] != "OK":
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
            raise Exception(msg)
   
        return data

    def load(self):
        domain = self.__call_api("")['domain']
        self.zone_file_with_error = domain['zone_file_with_error']
        self.error = domain['error']
        self.live_zone_file = domain['live_zone_file']
        self.ttl = domain['ttl']
        self.name = domain['name']
        self.id = domain['id']

    def destroy(self):
        """
            Destroy the droplet
        """
        self.__call_api("/destroy/")

    def create(self):
        """
            Create the droplet with object properties.
        """
        data = {
                "name": self.name,
                "ip_address": self.ip_address,
            }
        data = self.__call_api("new", data)
        if data:
            self.id = data['domain']['id']

    def get_records(self):
        """
            Returns a list of Record objects
        """
        records = []
        data = self.__call_api("/records/")
        for record_data in data['records']:
            record = Record(domain_id=record_data.pop('domain_id'),
                            id=record_data.pop('id'))
            for key, value in record_data.iteritems():
                setattr(record, key, value)
            record.client_id = self.client_id
            record.api_key = self.api_key
            records.append(record)
        return records
