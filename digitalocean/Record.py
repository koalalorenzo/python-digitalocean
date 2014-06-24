import requests
      
class Record(object):
    def __init__(self, domain_id, id="", client_id="", api_key=""):
        self.domain_id = domain_id
        self.id = id
        self.client_id = client_id
        self.api_key = api_key
        self.record_type = None
        self.name = None
        self.data = None
        self.priority = None
        self.port = None
        self.weight = None
        
    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/v1/domains/%s/records/%s%s" % (
                         self.domain_id, self.id, path), params=payload)
        data = r.json()
        self.call_response = data
        if data['status'] != "OK":            
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
            raise Exception(msg)
        return data

    def create(self):
        """
            Create a record for a domain
        """
        data = {
                "record_type": self.record_type,
                "data": self.data,
                "name": self.name,
                "priority": self.priority,
                "port": self.port,
                "weight": self.weight
            }
        data = self.__call_api("new", data)
        if data:
            self.id = data['record']['id']

    def destroy(self):
        """
            Destroy the record
        """
        self.__call_api("/destroy/")

    def save(self):
        """
            Save existing record
        """
        data = {
            "record_type": self.record_type,
            "data": self.data,
            "name": self.name,
            "priority": self.priority,
            "port": self.port,
            "weight": self.weight,
        }
        data = self.__call_api("/edit/", data)

    def load(self):
        record = self.__call_api("")
        if record:
            record = record[u'record']
            self.id = record['id']
            self.record_type = record[u'record_type']
            self.name = record[u'name']
            self.data = record[u'data']
            self.priority = record[u'priority']
            self.port = record[u'port']
            self.weight = record[u'weight']
