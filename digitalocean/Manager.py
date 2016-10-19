# -*- coding: utf-8 -*-
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

from .baseapi import BaseAPI
from .baseapi import GET
from .Droplet import Droplet
from .Region import Region
from .Size import Size
from .Image import Image
from .Domain import Domain
from .SSHKey import SSHKey
from .Action import Action
from .Account import Account
from .FloatingIP import FloatingIP
from .Volume import Volume

class Manager(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

    def get_data(self, *args, **kwargs):
        """
            Customized version of get_data to perform __check_actions_in_data.

            The default amount of elements per page defined is 200 as explained
            here: https://github.com/koalalorenzo/python-digitalocean/pull/78
        """
        params = {}
        if "params" in kwargs:
            params = kwargs["params"]

        if "per_page" not in params:
            params["per_page"] = 200

        kwargs["params"] = params
        data = super(Manager, self).get_data(*args, **kwargs)
        # if there are more elements available (total) than the elements per 
        # page, try to deal with pagination. Note: Breaking the logic on
        # multiple pages,
        if 'meta' in data and 'total' in data['meta']:
            if data['meta']['total'] > params['per_page']:
                return self.__deal_with_pagination(args[0], data, params)
            else:
                return data
        else:
            return data

    def __deal_with_pagination(self, url, data, params):
        """
            Perform multiple calls in order to have a full list of elements
            when the API are "paginated". (content list is divided in more
            than one page)
        """
        try:
            lastpage_url = data['links']['pages']['last']
            pages = parse_qs(urlparse(lastpage_url).query)['page'][0]
            key, values = data.popitem()
            for page in range(2, int(pages) + 1):
                params.update({'page': page})
                new_data = super(Manager, self).get_data(url, params=params)

                more_values = list(new_data.values())[0]
                for value in more_values:
                    values.append(value)
            data = {}
            data[key] = values
        except KeyError:  # No pages.
            pass

        return data

    def get_account(self):
        """
            Returns an Account object.
        """
        return Account.get_object(api_token=self.token)

    def get_all_regions(self):
        """
            This function returns a list of Region object.
        """
        data = self.get_data("regions/")
        regions = list()
        for jsoned in data['regions']:
            region = Region(**jsoned)
            region.token = self.token
            regions.append(region)
        return regions

    def get_all_droplets(self, tag_name=None):
        """
            This function returns a list of Droplet object.
        """
        if tag_name:
            params = {"tag_name": tag_name}
            data = self.get_data("droplets/", params=params)
        else:
            data = self.get_data("droplets/")

        droplets = list()
        for jsoned in data['droplets']:
            droplet = Droplet(**jsoned)
            droplet.token = self.token

            for net in droplet.networks['v4']:
                if net['type'] == 'private':
                    droplet.private_ip_address = net['ip_address']
                if net['type'] == 'public':
                    droplet.ip_address = net['ip_address']
            if droplet.networks['v6']:
                droplet.ip_v6_address = droplet.networks['v6'][0]['ip_address']

            if "backups" in droplet.features:
                droplet.backups = True
            else:
                droplet.backups = False
            if "ipv6" in droplet.features:
                droplet.ipv6 = True
            else:
                droplet.ipv6 = False
            if "private_networking" in droplet.features:
                droplet.private_networking = True
            else:
                droplet.private_networking = False

            droplets.append(droplet)

        return droplets

    def get_droplet(self, droplet_id):
        """
            Return a Droplet by its ID.
        """
        return Droplet.get_object(api_token=self.token, droplet_id=droplet_id)

    def get_all_sizes(self):
        """
            This function returns a list of Size object.
        """
        data = self.get_data("sizes/")
        sizes = list()
        for jsoned in data['sizes']:
            size = Size(**jsoned)
            size.token = self.token
            sizes.append(size)
        return sizes

    def get_images(self, private=False, type=None):
        """
            This function returns a list of Image object.
        """
        params = {}
        if private:
            params['private'] = 'true'
        if type:
            params['type'] = type
        data = self.get_data("images/", params=params)
        images = list()
        for jsoned in data['images']:
            image = Image(**jsoned)
            image.token = self.token
            images.append(image)
        return images

    def get_all_images(self):
        """
            This function returns a list of Image objects containing all
            available DigitalOcean images, both public and private.
        """
        images = self.get_images()
        return images

    def get_image(self, image_id):
        """
            Return a Image by its ID.
        """
        return Image.get_object(api_token=self.token, image_id=image_id)

    def get_my_images(self):
        """
            This function returns a list of Image objects representing
            private DigitalOcean images (e.g. snapshots and backups).
        """
        images = self.get_images(private=True)
        return images

    def get_global_images(self):
        """
            This function returns a list of Image objects representing
            public DigitalOcean images (e.g. base distribution images
            and 'One-Click' applications).
        """
        data = self.get_images()
        images = list()
        for i in data:
            if i.public:
                i.token = self.token
                images.append(i)
        return images

    def get_distro_images(self):
        """
            This function returns a list of Image objects representing
            public base distribution images.
        """
        images = self.get_images(type='distribution')
        return images


    def get_app_images(self):
        """
            This function returns a list of Image objectobjects representing
            public DigitalOcean 'One-Click' application images.
        """
        images = self.get_images(type='application')
        return images


    def get_all_domains(self):
        """
            This function returns a list of Domain object.
        """
        data = self.get_data("domains/")
        domains = list()
        for jsoned in data['domains']:
            domain = Domain(**jsoned)
            domain.token = self.token
            domains.append(domain)
        return domains

    def get_domain(self, domain_name):
        """
            Return a Domain by its domain_name
        """
        return Domain.get_object(api_token=self.token, domain_name=domain_name)

    def get_all_sshkeys(self):
        """
            This function returns a list of SSHKey object.
        """
        data = self.get_data("account/keys/")
        ssh_keys = list()
        for jsoned in data['ssh_keys']:
            ssh_key = SSHKey(**jsoned)
            ssh_key.token = self.token
            ssh_keys.append(ssh_key)
        return ssh_keys

    def get_ssh_key(self, ssh_key_id):
        """
            Return a SSHKey object by its ID.
        """
        return SSHKey.get_object(api_token=self.token, ssh_key_id=ssh_key_id)

    def get_action(self, action_id):
        """
            Return an Action object by a specific ID.
        """
        return Action.get_object(api_token=self.token, action_id=action_id)

    def get_all_floating_ips(self):
        """
            This function returns a list of FloatingIP objects.
        """
        data = self.get_data("floating_ips")
        floating_ips = list()
        for jsoned in data['floating_ips']:
            floating_ip = FloatingIP(**jsoned)
            floating_ip.token = self.token
            floating_ips.append(floating_ip)
        return floating_ips

    def get_floating_ip(self, ip):
        """
            Returns a of FloatingIP object by its IP address.
        """
        return FloatingIP.get_object(api_token=self.token, ip=ip)

    def get_all_volumes(self):
        """
            This function returns a list of Volume objects.
        """
        data = self.get_data("volumes")
        volumes = list()
        for jsoned in data['volumes']:
            volume = Volume(**jsoned)
            volume.token = self.token
            volumes.append(volume)
        return volumes

    def get_volume(self, volume_id):
        """
            Returns a Volume object by its ID.
        """
        return Volume.get_object(api_token=self.token, volume_id=volume_id)

    def __str__(self):
        return "<Manager>"
