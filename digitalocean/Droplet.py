import requests
from .Action import Action
from .baseapi import BaseAPI

class Droplet(BaseAPI):
    id = None
    name = None
    memory = None
    vcpus = None
    disk = None
    region = []
    status = None
    image = None
    size = None
    locked = None
    created_at = None
    status = None
    networks = []
    kernel = None
    backup_ids = []
    snapshot_ids = []
    action_ids = []
    features = []
    ip_address = None
    private_ip_address = None
    ip_v6_address = None
    ssh_keys = None
    backups = None
    ipv6 = None
    private_networking = None

    def __init__(self, *args, **kwargs):
        super(Droplet, self).__init__()

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def __check_actions_in_data(self, data):
        try:
            action_id = data['droplet']['action_ids'][0]
        except KeyError: # Some actions return a list of action items.
            action_id = data['action']['id']
        # Prepend the action id to the begining to be consistent with the API.
        self.action_ids.insert(0, action_id)

    def get_data(*args, **kwargs):
        """
            Customized version of get_data to perform __check_actions_in_data
        """
        data = super(Droplet, self).get_data(*args, **kwargs)
        if kwargs.has_key("type"):
            if kwargs["type"] == "POST":
                self.__check_actions_in_data(data)
        return data

    def load(self):
        droplets = self.get_data("droplets/%s" % self.id)
        droplet = droplets['droplet']

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
        data = self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'power_on'}
        )
        return data

    def shutdown(self):
        """
            shutdown the droplet
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'shutdown'}
        )

    def reboot(self):
        """
            restart the droplet
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'reboot'}
        )

    def power_cycle(self):
        """
            restart the droplet
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'power_cycle'}
        )

    def power_off(self):
        """
            restart the droplet
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'power_off'}
        )

    def reset_root_password(self):
        """
            reset the root password
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'password_reset'}
        )

    def resize(self, new_size):
        """
            resize the droplet to a new size
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={"type": "resize", "size": new_size}
        )

    def take_snapshot(self, snapshot_name):
        """
            Take a snapshot!
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={"type": "snapshot", "name": snapshot_name}
        )

    def restore(self, image_id):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={"type":"restore", "image": image_id}
        )

    def rebuild(self, image_id=None):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        if self.image_id and not image_id:
            image_id = self.image_id

        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={"type": "rebuild", "image": image_id}
        )

    def enable_backups(self):
        """
            Enable automatic backups (Not yet implemented in APIv2)
        """
        print("Not yet implemented in APIv2")

    def disable_backups(self):
        """
            Disable automatic backups
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'disable_backups'}
        )

    def destroy(self):
        """
            Destroy the droplet
        """
        return self.get_data(
            "droplets/%s" % self.id,
            type="DELETE"
        )

    def rename(self, name):
        """
            Rename the droplet
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'rename', 'name': name}
        )

    def enable_private_networking(self):
        """
           Enable private networking on an existing Droplet where available.
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'enable_private_networking'}
        )

    def enable_ipv6(self):
        """
            Enable IPv6 on an existing Droplet where available.
        """
        return self.get_data(
            "droplets/%s/actions/" % self.id,
            type="POST",
            params={'type': 'enable_ipv6'}
        )

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
                data['ssh_keys[]']= str(ssh_keys)
            elif type(ssh_keys) in [set, list, tuple, dict]:
                data['ssh_keys[]'] = ','.join(str(x) for x in ssh_keys)
            else:
                raise Exception("ssh_key_ids should be an integer or long number, a string, a set, a list/tuple or a ditionary ")

        if self.backups:
            data['backups'] = True

        if self.ipv6:
            data['ipv6'] = True

        if self.private_networking:
            data['private_networking'] = True

        data = self.get_data(
            "droplets/%s" % self.id,
            type="POST",
            params=data
        )

        if data:
            self.id = data['droplet']['id']

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