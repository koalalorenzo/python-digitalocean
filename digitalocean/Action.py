from .baseapi import BaseAPI

class Action(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.token = None
        self.status = None
        self.type = None
        self.started_at = None
        self.completed_at = None
        self.resource_id = None
        self.resource_type = None
        self.region = None

        super(Action, self).__init__(*args, **kwargs)

    def load(self):
        action = self.get_data("actions/%s" % self.id)
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
