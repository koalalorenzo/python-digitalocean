# -*- coding: utf-8 -*-
from .baseapi import BaseAPI
from .Droplet import Droplet
from .Region import Region
from .Size import Size
from .Image import Image
from .Domain import Domain
from .SSHKey import SSHKey
from .Action import Action
from .Account import Account


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

    def get_all_droplets(self):
        """
            This function returns a list of Droplet object.
        """
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

    def get_all_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.get_data("images/")
        images = list()
        for jsoned in data['images']:
            image = Image(**jsoned)
            image.token = self.token
            images.append(image)
        return images

    def get_image(self, image_id):
        """
            Return a Image by its ID.
        """
        return Image.get_object(api_token=self.token, image_id=image_id)

    def get_my_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.get_data("images/")
        images = list()
        for jsoned in data['images']:
            if not jsoned['public']:
                image = Image(**jsoned)
                image.token = self.token
                images.append(image)
        return images

    def get_global_images(self):
        """
            This function returns a list of Image object.
        """
        data = self.get_data("images/")
        images = list()
        for jsoned in data['images']:
            if jsoned['public']:
                image = Image(**jsoned)
                image.token = self.token
                images.append(image)
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

    def __str__(self):
        return "%s" % (self.token)
