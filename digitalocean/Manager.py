from .baseapi import BaseAPI
from .Droplet import Droplet
from .Region import Region
from .Size import Size
from .Image import Image
from .Domain import Domain
from .SSHKey import SSHKey


class Manager(BaseAPI):
    def __init__(self, token=""):
        super(Image, self).__init__()
        if token:
            self.token = token

    def get_data(*args, **kwargs):
        """
            Customized version of get_data to perform __check_actions_in_data
        """
        data = super(Droplet, self).get_data(*args, **kwargs)

        params = {}
        if kwargs.has_key("params"):
            params = kwargs['params']
        unpaged_data = self.__deal_with_pagination(args[0], data, params)

        return unpaged_data

    def __deal_with_pagination(self, url, data, params):
        """
            Perform multiple calls in order to have a full list of elements
            when the API are "paginated". (content list is divided in more
            than one page)
        """
        try:
            pages = data['links']['pages']['last'].split('=')[-1]
            key, values = data.popitem()
            for page in range(2, int(pages) + 1):
                params.update({'page': page})
                new_data = self.get_data(url, params=params)

                more_values = new_data.values()[0]
                for value in more_values:
                    values.append(value)
            data = {}
            data[key] = values
        except KeyError: # No pages.
            pass

        return data

    def get_all_regions(self):
        """
            This function returns a list of Region object.
        """
        data = self.get_data("/regions/")
        regions = list()
        for jsoned in data['regions']:
            region = Region()
            region.token = self.token
            region.slug = jsoned['slug']
            region.name = jsoned['name']
            region.sizes = jsoned['sizes']
            region.available = jsoned['available']
            region.features = jsoned['features']
            regions.append(region)
        return regions

    def get_all_droplets(self):
        """
            This function returns a list of Droplet object.
        """
        data = self.get_data("/droplets/")
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
        data = self.get_data("/sizes/")
        sizes = list()
        for jsoned in data['sizes']:
            size = Size()
            size.token = self.token
            size.slug = jsoned['slug']
            size.memory = jsoned['memory']
            size.vcpus = jsoned['vcpus']
            size.disk = jsoned['disk']
            size.transfer = jsoned['transfer']
            size.price_monthly = jsoned['price_monthly']
            size.price_hourly = jsoned['price_hourly']
            size.regions = jsoned['regions']
            sizes.append(size)
        return sizes

    def get_all_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.get_data("/images/")
        images = list()
        for jsoned in data['images']:
            image = Image()
            image.token = self.token
            image.id = jsoned['id']
            image.name = jsoned['name']
            image.distribution = jsoned['distribution']
            image.slug = jsoned['slug']
            image.public = jsoned['public']
            image.regions = jsoned['regions']
            image.created_at = jsoned['created_at']
            images.append(image)
        return images

    def get_my_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.get_data("/images/")
        images = list()
        for jsoned in data['images']:
            if not jsoned['public']:
                image = Image()
                image.token = self.token
                image.id = jsoned['id']
                image.name = jsoned['name']
                image.distribution = jsoned['distribution']
                image.slug = jsoned['slug']
                image.public = jsoned['public']
                image.regions = jsoned['regions']
                image.created_at = jsoned['created_at']
                images.append(image)
        return images

    def get_global_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.get_data("/images/")
        images = list()
        for jsoned in data['images']:
            if jsoned['public']:
                image = Image()
                image.token = self.token
                image.id = jsoned['id']
                image.name = jsoned['name']
                image.distribution = jsoned['distribution']
                image.slug = jsoned['slug']
                image.public = jsoned['public']
                image.regions = jsoned['regions']
                image.created_at = jsoned['created_at']
                images.append(image)
        return images

    def get_all_domains(self):
        """
            This function returns a list of Domain object.
        """
        data = self.get_data("/domains/")
        domains = list()
        for jsoned in data['domains']:
            domain = Domain()
            domain.zone_file = jsoned['zone_file']
            domain.ttl = jsoned['ttl']
            domain.name = jsoned['name']
            domain.token = self.token
            domains.append(domain)
        return domains

    def get_all_sshkeys(self):
        """
            This function returns a list of SSHKey object.
        """
        data = self.get_data("/account/keys/")
        ssh_keys = list()
        for jsoned in data['ssh_keys']:
            ssh_key = SSHKey()
            ssh_key.id = jsoned['id']
            ssh_key.name = jsoned['name']
            ssh_key.public_key = jsoned['public_key']
            ssh_key.fingerprint = jsoned['fingerprint']
            ssh_key.token = self.token
            ssh_keys.append(ssh_key)
        return ssh_keys
