# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, GET, POST, DELETE


class StickySesions(object):
    """
  "sticky_sessions": {
    "type": "cookies",
    "cookie_name": "DO_LB",
    "cookie_ttl_seconds": 300
  },
    """
    def __init__(self, type='none', cookie_name='DO_LB',
                 cookie_ttl_seconds=300):
        self.type = type
        if type is 'cookies':
            self.cookie_name = cookie_name
            self.cookie_ttl_seconds = cookie_ttl_seconds


class ForwardingRule(object):
    """
      {
        "entry_protocol": "http",
        "entry_port": 80,
        "target_protocol": "http",
        "target_port": 80,
        "certificate_id": "",
        "tls_passthrough": false
      },
    """
    def __init__(self, entry_protocol=None, entry_port=None,
                 target_protocol=None, target_port=None, certificate_id="",
                 tls_passthrough=False):
        self.entry_protocol = entry_protocol
        self.entry_port = entry_port
        self.target_protocol = target_protocol
        self.target_port = target_port
        self.certificate_id = certificate_id
        self.tls_passthrough = tls_passthrough
        # if certificate_id and tls_passthrough:
        #     raise ValueError('certificate_id and tls_passthrough are mutually exclusive')
        # elif certificate_id:
        #     self.certificate_id = certificate_id
        # else:
        #     self.tls_passthrough = tls_passthrough


class HealthCheck(object):
    """
    "health_check": {
    "protocol": "http",
    "port": 80,
    "path": "/",
    "check_interval_seconds": 10,
    "response_timeout_seconds": 5,
    "healthy_threshold": 5,
    "unhealthy_threshold": 3
  },
    """
    def __init__(self, protocol='http', port=80, path='/',
                 check_interval_seconds=10, response_timeout_seconds=5,
                 healthy_threshold=5, unhealthy_threshold=3):
        self.protocol = protocol
        self.port = port
        self.path = path
        self.check_interval_seconds = check_interval_seconds
        self.response_timeout_seconds = response_timeout_seconds
        self.healthy_threshold = healthy_threshold
        self.unhealthy_threshold = unhealthy_threshold


class LoadBalancer(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.name = None
        self.region = None
        self.algorithm = None
        self.forwarding_rules = []
        self.health_check = None
        self.sticky_sessions = None
        self.redirect_http_to_https = False
        self.droplet_ids = []
        self.tag = None
        self.status = None
        self.created_at = None

        super(LoadBalancer, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, id):
        """
            Class method that will return a LoadBalancer object by its ID.

            Args:
                api_token: str - token
                id: str - Load Balancer ID
        """
        load_balancer = cls(token=api_token, id=id)
        load_balancer.load()
        return load_balancer

    def load(self):
        """
            Load the LoadBalancer object from DigitalOcean.

            Requires self.id to be set.
        """
        data = self.get_data('load_balancers/%s' % self.id, type=GET)
        load_balancer = data['load_balancer']

        # Setting the attribute values
        for attr in load_balancer.keys():
            if attr == 'health_check':
                health_check = HealthCheck(**load_balancer['health_check'])
                setattr(self, attr, health_check)
            elif attr == 'sticky_sessions':
                sticky_ses = StickySesions(**load_balancer['sticky_sessions'])
                setattr(self, attr, sticky_ses)
            elif attr == 'forwarding_rules':
                rules = list()
                for rule in load_balancer['forwarding_rules']:
                    rules.append(ForwardingRule(**rule))
                setattr(self, attr, rules)
            else:
                setattr(self, attr, load_balancer[attr])

        return self

    def create(self, *args, **kwargs):
        """
            Creates a new LoadBalancer.

            Note: Every argument and parameter given to this method will be
            assigned to the object.

            Args:
                name (str): The Load Balancer's name
                region (str): The slug identifier for a DigitalOcean region
                algorithm (str, optional): The load balancing algorithm used
                forwarding_rules (obj:`list`): A list of ForwrdingRules objects
                health_check (obj, optional):
                sticky_sessions (obj, optional):
                redirect_http_to_https (bool, optional):
                droplet_ids (obj:`list` of `int`):
                tag (str):
        """
        rules_dict = [rule.__dict__ for rule in self.forwarding_rules]

        params = {'name': self.name, 'region': self.region,
                  'forwarding_rules': rules_dict,
                  'redirect_http_to_https': self.redirect_http_to_https}

        if self.droplet_ids and self.tag:
            raise ValueError('droplet_ids and tag are mutually exclusive args')
        elif self.tag:
            params['tag'] = self.tag
        else:
            params['droplet_ids'] = self.droplet_ids

        if self.algorithm:
            params['algorithm'] = self.algorithm
        if self.health_check:
            params['health_check'] = self.health_check.__dict__
        if self.sticky_sessions:
            params['sticky_sessions'] = self.sticky_sessions.__dict__

        data = self.get_data('load_balancers/', type=POST, params=params)

        if data:
            self.id = data['load_balancer']['id']
            self.ip = data['load_balancer']['ip']
            self.algorithm = data['load_balancer']['algorithm']
            self.health_check = data['load_balancer']['health_check']  # FIXME
            self.sticky_sessions = data['load_balancer']['sticky_sessions']  # FIXME
            self.droplet_ids = data['load_balancer']['droplet_ids']
            self.status = data['load_balancer']['status']
            self.created_at = data['load_balancer']['created_at']

        return self

    def destroy(self):
        """
            Destroy the LoadBalancer
        """
        return self.get_data('load_balancers/%s/' % self.id, type=DELETE)

    def add_droplets(self, droplet_ids):
        """
            Assign a LoadBalancer to a Droplet.

            Args:
                droplet_ids (obj:`list` of `int`): A list of Droplet IDs
        """
        return self.get_data(
            "load_balancers/%s/droplets/" % self.id,
            type=POST,
            params={"droplet_ids": droplet_ids}
        )

    def remove_droplets(self, droplet_ids):
        """
            Unassign a LoadBalancer.
        """
        return self.get_data(
            "load_balancers/%s/droplets/" % self.id,
            type=DELETE,
            params={"droplet_ids": droplet_ids}
        )

    def add_forwarding_rules(self, forwarding_rules):
        """
            Assign a LoadBalancer to a Droplet.

            Args:
                droplet_ids (obj:`list` of `int`): A list of Droplet IDs
        """
        rules_dict = [rule.__dict__ for rule in forwarding_rules]
        print rules_dict
        return self.get_data(
            "load_balancers/%s/forwarding_rules/" % self.id,
            type=POST,
            params={"forwarding_rules": rules_dict}
        )

    def remove_forwarding_rules(self, forwarding_rules):
        """
            Assign a LoadBalancer to a Droplet.

            Args:
                droplet_ids (obj:`list` of `int`): A list of Droplet IDs
        """
        rules_dict = [rule.__dict__ for rule in forwarding_rules]

        return self.get_data(
            "load_balancers/%s/forwarding_rules/" % self.id,
            type=DELETE,
            params={"forwarding_rules": rules_dict}
        )

    def __str__(self):
        return "%s" % (self.id)
