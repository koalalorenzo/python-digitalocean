import requests

class Action(object):
    def __init__(self, action_id=""):
        self.id = action_id
        self.token = None
        self.status = None
        self.type = None
        self.started_at = None
        self.completed_at = None
        self.resource_id = None
        self.resource_type = None
        self.region = None

    def __call_api(self, path, params=dict()):
        payload = {}
        headers = {'Authorization':'Bearer ' + self.token}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/v2/actions/%s" % self.id,
                         headers=headers,
                         params=payload)
        data = r.json()
        self.call_response = data
        if r.status_code != requests.codes.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise Exception(msg)
        return data

    def load(self):
        action = self.__call_api('')
        if action:
            action = action[u'action']
            self.id = action[u'id']
            self.status = action[u'status']
            self.type = action[u'type']
            self.started_at = action[u'started_at']
            self.completed_at = action[u'completed_at']
            self.resource_id = action[u'resource_id']
            self.resource_typ = action[u'resource_type']
            self.region = action[u'region']
