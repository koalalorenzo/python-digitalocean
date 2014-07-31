import requests
from .Action import Action

class Droplet(object):
    def __init__(self, *args, **kwargs):
        self.token = ""
        self.id = None
        self.name = None
        self.memory = None
        self.vcpus = None
        self.disk = None
        self.region = []
        self.status = None
        self.image = None
        self.size = None
        self.locked = None
        self.created_at = None
        self.status = None
        self.networks = []
        self.kernel = None
        self.backup_ids = []
        self.snapshot_ids = []
        self.action_ids = []
        self.features = []
        self.ip_address = None
        self.private_ip_address = None
        self.ip_v6_address = None
        self.ssh_keys = None
        self.backups = None
        self.ipv6 = None
        self.private_networking = None

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def call_api(self, type, path, params=dict()):
        """
            exposes any api entry
            useful when working with new API calls that are not yet implemented by Droplet class
        """
        return self.__call_api(type, path, params)

    def __call_api(self, type, path, params=dict()):
        payload = {}
        headers = {'Authorization': 'Bearer ' + self.token}
        payload.update(params)
        if not self.id:
            self.id = ''
        if type == 'POST':
            headers['content-type'] = 'application/json'
            r = requests.post("https://api.digitalocean.com/v2/droplets/%s%s" %
                             (self.id, path),
                              headers=headers,
                              params=payload)
        if type == 'DELETE':
            headers['content-type'] = 'application/x-www-form-urlencoded'
            r = requests.delete("https://api.digitalocean.com/v2/droplets/%s" %
                             (self.id),
                              headers=headers,
                              params=payload)
        else:
            r = requests.get("https://api.digitalocean.com/v2/droplets/%s%s" %
                            (self.id, path),
                             headers=headers,
                             params=payload)

        # A successful delete returns "204 No Content"
        if r.status_code != 204:
            data = r.json()
            self.call_response = data
            if r.status_code != requests.codes.ok:
                msg = [data[m] for m in ("id", "message") if m in data][1]
                raise Exception(msg)

        # Add the action to the object's action list.
        if type == 'POST': # Actions are only returned for POST's.
            try: # Creates return a list of droplets
                action_id = data['droplets'][-1]['action_ids'][0]
            except KeyError: # Other actions return a list of action items.
                action_id = data['actions'][0]['id']
            # Prepend the action id to the begining to be consistent with the API.
            self.action_ids.insert(0, action_id)

        return data

    def load(self):
        droplet = self.__call_api('GET', '')['droplet']
        self.id = droplet['id']
        self.name = droplet['name']
        self.memory = droplet['memory']
        self.vcpus = droplet['vcpus']
        self.disk = droplet['disk']
        self.region = droplet['region']
        self.status = droplet['status']
        self.image = droplet['image']
        self.size = droplet['size']
        self.locked = droplet['locked']
        self.created_at = droplet['created_at']
        self.status = droplet['status']
        self.networks = droplet['networks']
        self.kernel = droplet['kernel']
        self.backup_ids = droplet['backup_ids']
        self.snapshot_ids = droplet['snapshot_ids']
        self.action_ids = droplet['action_ids']
        self.features = droplet['features']
        for net in self.networks['v4']:
            if net['type'] == 'private':
                self.private_ip_address = net['ip_address']
            if net['type'] == 'public':
                self.ip_address = net['ip_address']
        if self.networks['v6']:
            self.ip_v6_address = droplet.networks['v6'][0]['ip_address']
        return self

    def power_on(self):
        """
            Boot up the droplet
        """
        self.__call_api('POST', '/actions/', {'type': 'power_on'})

    def shutdown(self):
        """
            shutdown the droplet
        """
        self.__call_api('POST', '/actions/', {'type': 'shutdown'})

    def reboot(self):
        """
            restart the droplet
        """
        self.__call_api('POST', '/actions/', {'type': 'reboot'})

    def power_cycle(self):
        """
            restart the droplet
        """
        self.__call_api('POST', '/actions/', {'type': 'power_cycle'})

    def power_off(self):
        """
            restart the droplet
        """
        self.__call_api('POST', '/actions/', {'type': 'power_off'})

    def reset_root_password(self):
        """
            reset the root password
        """
        self.__call_api('POST', '/actions/', {'type': 'password_reset'})

    def resize(self, new_size):
        """
            resize the droplet to a new size
        """
        self.__call_api("POST", "/actions/", {"type": "resize", "size": new_size})

    def take_snapshot(self, snapshot_name):
        """
            Take a snapshot!
        """
        self.__call_api("POST", "/actions/", {"type": "snapshot", "name": snapshot_name})

    def restore(self, image_id):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        self.__call_api("POST", "/actions/", {"type":"restore", "image": image_id})

    def rebuild(self, image_id=None):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        if self.image_id and not image_id:
            image_id = self.image_id
        self.__call_api("POST", "/actions/", {"type": "rebuild", "image": image_id})

    def enable_backups(self):
        """
            Enable automatic backups (Not yet implemented in APIv2)
        """
        print("Not yet implemented in APIv2")

    def disable_backups(self):
        """
            Disable automatic backups
        """
        self.__call_api("POST", "/actions/", {'type': 'disable_backups'})

    def destroy(self):
        """
            Destroy the droplet
        """
        self.__call_api("DELETE", "")

    def rename(self, name):
        """
            Rename the droplet
        """
        self.__call_api("POST", "/actions/", {'type': 'rename', 'name': name})

    def enable_private_networking(self):
        """
           Enable private networking on an existing Droplet where available.
        """
        self.__call_api("POST", "/actions/", {'type': 'enable_private_networking'})

    def enable_ipv6(self):
        """
            Enable IPv6 on an existing Droplet where available.
        """
        self.__call_api("POST", "/actions/", {'type': 'enable_ipv6'})

    def create(self, ssh_keys=None, backups=False, ipv6=False, private_networking=False):
        """
            Create the droplet with object properties.
        """
        data = {
                "name": self.name,
                "size": self.size,
                "image": self.image,
                "region": self.region,
                "ssh_keys": self.ssh_keys
            }

        if ssh_keys:
            if type(ssh_keys) in [int, long, str]:
                data['ssh_keys']= str(ssh_keys)
            elif type(ssh_keys) in [set, list, tuple, dict]:
                data['ssh_keys'] = ','.join(str(x) for x in ssh_keys)
            else:
                raise Exception("ssh_key_ids should be an integer or long number, a string, a set, a list/tuple or a ditionary ")

        if self.backups:
            data['backups'] = True

        if self.ipv6:
            data['ipv6'] = True

        if self.private_networking:
            data['private_networking'] = True

        data = self.__call_api("POST", "", data)
        if data:
            self.id = data['droplets'][-1]['id']

    def get_events(self):
        """
            A helper function for backwards compatability.
            Calls get_actions()
        """
        return self.get_actions()

    def get_actions(self):
        """
            Returns a list of Action objects
            This actions can be used to check the droplet's status
        """
        actions = []
        for action_id in self.action_ids:
            action = Action(action_id)
            action.token = self.token
            action.load()
            actions.append(action)
        return actions