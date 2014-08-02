import requests
from .Record import Record

class Domain(object):
    def __init__(self, *args, **kwargs):
        self.token = ""
        self.name = None
        self.ttl = None
        self.zone_file = None
        ip_address = None

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def __call_api(self, type, path, params=dict()):
        payload = {}
        headers = {'Authorization':'Bearer ' + self.token}
        payload.update(params)
        if type == 'POST':
            print "POSTing"
            headers['content-type'] = 'application/json'
            r = requests.post("https://api.digitalocean.com/v2/domains%s" %
                              path,
                              headers=headers,
                              params=payload)
        elif type == 'DELETE':
            headers['content-type'] = 'application/x-www-form-urlencoded'
            r = requests.delete("https://api.digitalocean.com/v2/domains%s" %
                              path,
                              headers=headers,
                              params=payload)
        else:
            r = requests.get("https://api.digitalocean.com/v2/domains%s" %
                              path,
                              headers=headers,
                              params=payload)
        print r.status_code, r.url
        # A successful delete returns "204 No Content"
        print r.status_code
        if r.status_code != 204:
            data = r.json()
            print data
            self.call_response = data
            if r.status_code not in [requests.codes.ok, 202, 201]:
                msg = [data[m] for m in ("id", "message") if m in data][1]
                raise Exception(msg)
   
            return data

    def load(self):
        domain = self.__call_api("GET", "")['domain']
        self.live_zone_file = domain['zone_file']
        self.ttl = domain['ttl']
        self.name = domain['name']

    def delete(self):
        """
            Destroy the domain by name
        """
        self.__call_api("DELETE", '/' + self.name)

    def create(self):
        """
            Create new doamin
        """
        data = {
                "name": self.name,
                "ip_address": self.ip_address,
            }
        data = self.__call_api("POST", "", data)

    def get_records(self):
        """
            Returns a list of Record objects
        """
        records = []
        data = self.__call_api("GET", "/records/")
        for record_data in data['records']:
            record = Record(domain_id=record_data.pop('domain_id'),
                            id=record_data.pop('id'))
            for key, value in record_data.iteritems():
                setattr(record, key, value)
            record.client_id = self.client_id
            record.api_key = self.api_key
            records.append(record)
        return records
