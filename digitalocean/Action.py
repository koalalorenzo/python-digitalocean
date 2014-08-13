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
            # Loading attributes
            for attr in action.keys():
                setattr(self,attr,action[attr])
