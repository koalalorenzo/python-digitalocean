import requests

class Event(object):
    def __init__(self, event_id="", client_id="", api_key=""):
        self.id = event_id
        self.client_id = client_id
        self.api_key = api_key
        self.event_type_id = None
        self.percentage = None
        self.droplet_id = None
        self.action_status = None
        self.load()
        
    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/events/%s%s" % ( self.id, path ), params=payload)
        data = r.json()
        if data['status'] != "OK":
            return None # Raise?
        return data

    def load(self):
        event = self.__call_api("")
        if event:
            event = event.get(u'event')
            self.id = event['id']
            self.event_type_id = event[u'event_type_id']
            self.percentage = event[u'percentage']
            self.droplet_id = event[u'droplet_id']
            self.action_status = event[u'action_status']
        