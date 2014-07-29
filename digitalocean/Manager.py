import requests
from .Droplet import Droplet
from .Region import Region
from .Size import Size
from .Image import Image
from .Domain import Domain
from .SSHKey import SSHKey


class Manager(object):
    def __init__(self, token=""):
        self.token = token
        self.call_response = None

    def __call_api(self, path, params=dict()):
        payload = {}
        headers = {'Authorization':'Bearer ' + self.token}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/v2/%s" % path,
                         headers=headers,
                         params=payload)
        data = r.json()
        self.call_response = data
        if r.status_code != requests.codes.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise Exception(msg)
        return data

    def get_all_regions(self):
        """
            This function returns a list of Region object.
        """
        data = self.__call_api("/regions/")
        regions = list()
        for jsoned in data['regions']:
            region = Region()
            region.id = jsoned['id']
            region.name = jsoned['name']
            region.client_id = self.client_id
            region.api_key = self.api_key
            regions.append(region)
        return regions

    def get_all_droplets(self):
        """
            This function returns a list of Droplet object.
        """
        data = self.__call_api("/droplets/")
        droplets = list()
        for jsoned in data['droplets']:
            droplet = Droplet()
            droplet.token = self.token
            droplet.id = jsoned['id']
            droplet.name = jsoned['name']
            droplet.memory = jsoned['memory']
            droplet.vcpus = jsoned['vcpus']
            droplet.disk = jsoned['disk']
            droplet.region = jsoned['region']
            droplet.status = jsoned['status']
            droplet.image = jsoned['image']
            droplet.size = jsoned['size']
            droplet.locked = jsoned['locked']
            droplet.created_at = jsoned['created_at']
            droplet.status = jsoned['status']
            droplet.networks = jsoned['networks']
            droplet.kernel = jsoned['kernel']
            droplet.backup_ids = jsoned['backup_ids']
            droplet.snapshot_ids = jsoned['snapshot_ids']
            droplet.action_ids = jsoned['action_ids']
            droplet.features = jsoned['features']
            for net in droplet.networks['v4']:
                if net['type'] == 'private':
                    droplet.private_ip_address = net['ip_address']
                if net['type'] == 'public':
                    droplet.ip_address = net['ip_address']
            if droplet.networks['v6']:
                droplet.ip_v6_address = droplet.networks['v6'][0]['ip_address']
            droplets.append(droplet)
        return droplets

    def get_all_sizes(self):
        """
            This function returns a list of Size object.
        """
        data = self.__call_api("/sizes/")
        sizes = list()
        for jsoned in data['sizes']:
            size = Size()
            size.id = jsoned['id']
            size.name = jsoned['name']
            size.memory = jsoned['memory']
            size.cpu = jsoned['cpu']
            size.disk = jsoned['disk']
            size.cost_per_hour = jsoned['cost_per_hour']
            size.cost_per_month = jsoned['cost_per_month']
            size.client_id = self.client_id
            size.api_key = self.api_key
            sizes.append(size)
        return sizes

    def get_all_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.__call_api("/images/")
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.client_id = self.client_id
            image.api_key = self.api_key
            images.append(image)
        return images

    def get_my_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.__call_api("/images/",{"filter":"my_images"})
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.client_id = self.client_id
            image.api_key = self.api_key
            images.append(image)
        return images

    def get_global_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.__call_api("/images/",{"filter":"global"})
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.client_id = self.client_id
            image.api_key = self.api_key
            images.append(image)
        return images

    def get_all_domains(self):
        """
            This function returns a list of Domain object.
        """
        data = self.__call_api("/domains/")
        domains = list()
        for jsoned in data['domains']:
            domain = Domain()
            domain.zone_file_with_error = jsoned['zone_file_with_error']
            domain.error = jsoned['error']
            domain.live_zone_file = jsoned['live_zone_file']
            domain.ttl = jsoned['ttl']
            domain.name = jsoned['name']
            domain.id = jsoned['id']
            domain.client_id = self.client_id
            domain.api_key = self.api_key
            domains.append(domain)
        return domains

    def get_all_sshkeys(self):
        """
            This function returns a list of SSHKey object.
        """
        data = self.__call_api("/ssh_keys/")
        ssh_keys = list()
        for jsoned in data['ssh_keys']:
            ssh_key = SSHKey()
            ssh_key.id = jsoned['id']
            ssh_key.name = jsoned['name']
            ssh_key.client_id = self.client_id
            ssh_key.api_key = self.api_key
            ssh_keys.append(ssh_key)
        return ssh_keys

