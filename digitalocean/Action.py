# -*- coding: utf-8 -*-
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
        # Custom, not provided by the json object.
        self.droplet_id = None

        super(Action, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, action_id):
        """
            Class method that will return a Action object by ID.
        """
        action = cls(token=api_token, id=action_id)
        action.load_directly()
        return action

    def load_directly(self):
        action = self.get_data("actions/%s" % self.id)
        if action:
            action = action[u'action']
            # Loading attributes
            for attr in action.keys():
                setattr(self, attr, action[attr])

    def load(self):
        action = self.get_data(
            "droplets/%s/actions/%s" % (
                self.droplet_id,
                self.id
            )
        )
        if action:
            action = action[u'action']
            # Loading attributes
            for attr in action.keys():
                setattr(self, attr, action[attr])

    def __str__(self):
        return "%s %s [%s]" % (self.id, self.type, self.status)
