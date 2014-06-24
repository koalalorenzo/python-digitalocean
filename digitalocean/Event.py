import requests

class Event(object):
    def __init__(self, event_id=""):
        self.id = event_id
        self.client_id = None
        self.api_key = None
        self.event_type_id = None
        self.percentage = None
        self.droplet_id = None
        self.action_status = None
        self.call_response = None
        
    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/v1/events/%s%s" % ( self.id, path ), params=payload)
        data = r.json()
        self.call_response = data
        if data['status'] != "OK":            
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
            raise Exception(msg)
        return data

    def load(self):
        event = self.__call_api("")
        if event:
            event = event[u'event']
            self.id = event['id']
            self.event_type_id = event[u'event_type_id']
            self.percentage = event[u'percentage']
            self.droplet_id = event[u'droplet_id']
            self.action_status = event[u'action_status']
        
