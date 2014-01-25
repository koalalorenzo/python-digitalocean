import requests
from .Droplet import Droplet
from .Region import Region
from .Size import Size
from .Image import Image
from .Domain import Domain
from .SSHKey import SSHKey


class Manager(object):
    def __init__(self, client_id="", api_key=""):
        self.client_id = client_id
        self.api_key = api_key
        self.call_response = None

    def __call_api(self, path, params=dict()):
        payload = {'client_id': self.client_id, 'api_key': self.api_key}
        payload.update(params)
        r = requests.get("https://api.digitalocean.com/%s" % path, params=payload)
        data = r.json()
        self.call_response = data
        if data['status'] != "OK":
            msg = [data[m] for m in ("message", "error_message", "status") if m in data][0]
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
            droplet.backup_active = jsoned['backups_active']
            droplet.region_id = jsoned['region_id']
            droplet.size_id = jsoned['size_id']
            droplet.image_id = jsoned['image_id']
            droplet.status = jsoned['status']
            droplet.name = jsoned['name']
            droplet.id = jsoned['id']
            droplet.ip_address = jsoned['ip_address']
            droplet.private_ip_address = jsoned['private_ip_address']
            droplet.client_id = self.client_id
            droplet.api_key = self.api_key
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

