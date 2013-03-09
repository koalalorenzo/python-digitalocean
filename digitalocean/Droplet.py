import requests

class Droplet(object):
    def __init__(self, droplet_id="", client_id="", api_key=""):
        self.id = droplet_id
        self.client_id = client_id
        self.api_key = api_key

        self.name = None
        self.backup_active = None
        self.region_id = None
        self.image_id = None
        self.size_id = None
        self.status = None

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/droplets/%s%s" % ( self.id, path ), params=payload)
        data = r.json()
        if data['status'] != "OK":
            return None # Raise?
        return data

    def load(self):
        droplet = self.__call_api("")['droplet']
        self.backup_active = droplet['backups_active']
        self.region_id = droplet['region_id']
        self.size_id = droplet['size_id']
        self.image_id = droplet['image_id']
        self.status = droplet['status']
        self.name = droplet['name']
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

    def destroy(self):
        """
            Destroy the droplet
        """
        self.__call_api("/destroy/")

    def create(self):
        """
            Create the droplet with object properties.
        """
        data = {
                "name": self.name,
                "size_id": self.size_id,
                "image_id": self.image_id,
                "region_id": self.region_id
            }
        self.__call_api("/new", data)
