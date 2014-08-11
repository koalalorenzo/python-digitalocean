from .baseapi import BaseAPI

class Action(BaseAPI):
    id = None
    token = None
    status = None
    type = None
    started_at = None
    completed_at = None
    resource_id = None
    resource_type = None
    region = None

    def __init__(self, action_id=""):
        super(Action, self).__init__()
        if action_id:
            self.id = action_id

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
