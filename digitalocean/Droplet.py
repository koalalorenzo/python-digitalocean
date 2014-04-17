import requests
from .Event import Event

class Droplet(object):
    def __init__(self, *args, **kwargs):
        self.id = ""
        self.client_id = ""
        self.api_key = ""
        self.name = None
        self.backup_active = None
        self.region_id = None
        self.image_id = None
        self.size_id = None
        self.status = None
        self.ip_address = None
        self.private_ip_address = None
        self.call_reponse = None
        self.ssh_key_ids = None
        self.events = []

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def call_api(self, path, params=dict()):
        """
            exposes any api entry
            useful when working with new API calls that are not yet implemented by Droplet class
        """
        return self.__call_api(path, params)

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/droplets/%s%s" % ( self.id, path ), params=payload)
        data = r.json()
        self.call_response = data
        if data['status'] != "OK":
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
            raise Exception(msg)
        #add the event to the object's event list.
        event_id = data.get(u'event_id',None)
        if not event_id and u'event_id' in data.get(u'droplet',{}):
            event_id = data[u'droplet'][u'event_id']

        if event_id: self.events.append(event_id)
        return data

    def load(self):
        droplet = self.__call_api("")['droplet']
        self.backup_active = droplet['backups_active']
        self.region_id = droplet['region_id']
        self.size_id = droplet['size_id']
        self.image_id = droplet['image_id']
        self.status = droplet['status']
        self.name = droplet['name']
        self.ip_address = droplet['ip_address']
        self.private_ip_address = droplet['private_ip_address']
        self.id = droplet['id']

    def power_on(self):
        """
            Boot up the droplet
        """
        self.__call_api("/power_on/")

    def shutdown(self):
        """
            shutdown the droplet
        """
        self.__call_api("/shutdown/")

    def reboot(self):
        """
            restart the droplet
        """
        self.__call_api("/reboot/")

    def power_cycle(self):
        """
            restart the droplet
        """
        self.__call_api("/power_cycle/")

    def power_off(self):
        """
            restart the droplet
        """
        self.__call_api("/power_off/")

    def reset_root_password(self):
        """
            reset the root password
        """
        self.__call_api("/reset_root_password/")

    def resize(self, new_size):
        """
            resize the droplet to a new size
        """
        self.__call_api("/resize/", {"size_id": new_size})

    def take_snapshot(self, snapshot_name):
        """
            Take a snapshot!
        """
        self.__call_api("/snapshot/", {"name": snapshot_name})

    def restore(self, image_id):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        self.__call_api("/restore/", {"image_id": image_id})

    def rebuild(self, image_id=None):
        """
            Restore the droplet to an image ( snapshot or backup )
        """
        if self.image_id and not image_id:
            image_id = self.image_id
        self.__call_api("/rebuild/", {"image_id": image_id})

    def enable_backups(self):
        """
            Enable automatic backups
        """
        self.__call_api("/enable_backups/")

    def disable_backups(self):
        """
            Disable automatic backups
        """
        self.__call_api("/disable_backups/")

    def destroy(self, scrub_data=True):
        """
            Destroy the droplet
        """
        self.__call_api("/destroy/", {'scrub_data': '1' if scrub_data else '0'})

    def rename(self, name):
        """
            Rename the droplet
        """
        self.__call_api("/rename/", {'name': name})

    def create(self, ssh_key_ids=None, virtio=False, private_networking=False, backups_enabled=False):
        """
            Create the droplet with object properties.
        """
        data = {
                "name": self.name,
                "size_id": self.size_id,
                "image_id": self.image_id,
                "region_id": self.region_id,
                "ssh_key_ids": self.ssh_key_ids
            }

        if ssh_key_ids:
            if type(ssh_key_ids) in [int, long, str]:
                data['ssh_key_ids']= str(ssh_key_ids)
            elif type(ssh_key_ids) in [set, list, tuple, dict]:
                data['ssh_key_ids'] = ','.join(str(x) for x in ssh_key_ids)
            else:
                raise Exception("ssh_key_ids should be an integer or long number, a string, a set, a list/tuple or a ditionary ")

        if backups_enabled:
            data['backups_enabled'] = 1

        if virtio:
            data['virtio'] = 1

        if private_networking:
            data['private_networking'] = 1

        data = self.__call_api("new", data)
        if data:
            self.id = data['droplet']['id']

    def get_events(self):
        """
            Returns a list of Event objects
            This events can be used to check the droplet's status
        """
        events = []
        for event_id in self.events:
            event = Event(event_id)
            event.client_id = self.client_id
            event.api_key = self.api_key
            event.load()
            events.append(event)
        return events
