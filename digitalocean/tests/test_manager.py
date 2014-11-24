import os
import unittest
import responses

import digitalocean

class TestManager(unittest.TestCase):

    def load_from_file(self, json_file):
        cwd = os.path.dirname(__file__)
        with open(os.path.join(cwd, 'data/%s' % json_file), 'r') as f:
            return f.read()

    def setUp(self):
        self.base_url = "https://api.digitalocean.com/v2/"
        self.token = "afaketokenthatwillworksincewemockthings"
        self.manager = digitalocean.Manager(token=self.token)

    @responses.activate
    def test_auth_fail(self):
        data = self.load_from_file('errors/unauthorized.json')

        url = self.base_url + 'regions/'
        responses.add(responses.GET, url,
                      body=data,
                      status=401,
                      content_type='application/json')

        bad_token = digitalocean.Manager(token='thisisnotagoodtoken')
        with self.assertRaises(Exception) as error:
            bad_token.get_all_regions()

        exception = error.exception
        self.assertEqual(exception.message, 'Unable to authenticate you.')

    @responses.activate
    def test_droplets(self):
        data = self.load_from_file('droplets/all.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        droplets = self.manager.get_all_droplets()

        droplet = droplets[0]
        self.assertEqual(droplet.token, self.token)
        self.assertEqual(droplet.id, 3164444)
        self.assertEqual(droplet.name, "example.com")
        self.assertEqual(droplet.memory, 512)
        self.assertEqual(droplet.vcpus, 1)
        self.assertEqual(droplet.disk, 20)
        self.assertEqual(droplet.region['slug'], "nyc3")
        self.assertEqual(droplet.status, "active")
        self.assertEqual(droplet.image['slug'], "ubuntu-14-04-x64")
        self.assertEqual(droplet.size_slug, '512mb')
        self.assertEqual(droplet.created_at, "2014-11-14T16:29:21Z")
        self.assertEqual(droplet.ip_address, "104.236.32.182")
        self.assertEqual(droplet.ip_v6_address,
                "2604:A880:0800:0010:0000:0000:02DD:4001")
        self.assertEqual(droplet.kernel['id'], 2233)
        self.assertEqual(droplet.backup_ids, [7938002])
        self.assertEqual(droplet.features, ["backups",
                                            "ipv6",
                                            "virtio"])

    @responses.activate
    def test_get_all_regions(self):
        data = self.load_from_file('regions/all.json')

        url = self.base_url + 'regions/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_regions = self.manager.get_all_regions()
        self.assertEqual(len(all_regions), 3)

        region = all_regions[0]
        self.assertEqual(region.token, self.token)
        self.assertEqual(region.name, 'New York')
        self.assertEqual(region.slug, 'nyc1')
        self.assertEqual(region.sizes,["1gb", "512mb"])
        self.assertEqual(region.features, ['virtio',
                                           'private_networking',
                                           'backups',
                                           'ipv6'])

    @responses.activate
    def test_get_all_sizes(self):
        data = self.load_from_file('sizes/all.json')

        url = self.base_url + 'sizes/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_sizes = self.manager.get_all_sizes()
        self.assertEqual(len(all_sizes), 2)

        size = all_sizes[0]
        self.assertEqual(size.token, self.token)
        self.assertEqual(size.slug, '512mb')
        self.assertEqual(size.memory, 512)
        self.assertEqual(size.disk, 20)
        self.assertEqual(size.price_hourly, 0.00744)
        self.assertEqual(size.price_monthly, 5.0)
        self.assertEqual(size.transfer, 1)
        self.assertEqual(size.regions, ["nyc1", "ams1", "sfo1"])

    @responses.activate
    def test_get_all_images(self):
        data = self.load_from_file('images/all.json')

        url = self.base_url + 'images/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_images = self.manager.get_all_images()
        self.assertEqual(len(all_images), 3)

        image = all_images[0]
        self.assertEqual(image.token, self.token)
        self.assertEqual(image.id, 119192817) 
        self.assertEqual(image.name, '14.04 x64')
        self.assertTrue(image.public)
        self.assertEqual(image.slug, "ubuntu-14-04-x64")
        self.assertEqual(image.distribution, 'Ubuntu')
        self.assertEqual(image.regions, ['nyc1'])
        self.assertEqual(image.created_at, "2014-07-29T14:35:40Z")

    @responses.activate
    def test_get_global_images(self):
        data = self.load_from_file('images/all.json')

        url = self.base_url + 'images/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        global_images = self.manager.get_global_images()
        self.assertEqual(len(global_images), 2)

        image = global_images[0]
        self.assertEqual(image.token, self.token)
        self.assertEqual(image.id, 119192817) 
        self.assertEqual(image.name, '14.04 x64')
        self.assertTrue(image.public)
        self.assertEqual(image.slug, "ubuntu-14-04-x64")
        self.assertEqual(image.distribution, 'Ubuntu')
        self.assertEqual(image.regions, ['nyc1'])
        self.assertEqual(image.created_at, "2014-07-29T14:35:40Z")

    @responses.activate
    def test_get_my_images(self):
        data = self.load_from_file('images/all.json')

        url = self.base_url + 'images/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        my_images = self.manager.get_my_images()
        self.assertEqual(len(my_images), 1)

        image = my_images[0]
        self.assertEqual(image.token, self.token)
        self.assertEqual(image.id, 449676856) 
        self.assertEqual(image.name, 'My Snapshot')
        self.assertFalse(image.public)
        self.assertEqual(image.slug, "")
        self.assertEqual(image.distribution, 'Ubuntu')
        self.assertEqual(image.regions, ['nyc1', 'nyc3'])
        self.assertEqual(image.created_at, "2014-08-18T16:35:40Z")

    @responses.activate
    def test_get_all_sshkeys(self):
        data = self.load_from_file('keys/all.json')

        url = self.base_url + 'account/keys/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        ssh_keys = self.manager.get_all_sshkeys()
        self.assertEqual(len(ssh_keys), 1)

        # Test the few things we can assume about a random ssh key.
        key = ssh_keys[0]
        self.assertEqual(key.token, self.token)
        self.assertEqual(key.name, "Example Key")
        self.assertEqual(key.id, 1)
        self.assertEqual(key.public_key,
            "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQDGk5V68BJ4P3Ereh779Vi/Ft2qs/rbXrcjKLGo6zsyeyFUE0svJUpRDEJvFSf8RlezKx1/1ulJu9+kZsxRiUKn example")
        self.assertEqual(key.fingerprint,
            "f5:d1:78:ed:28:72:5f:e1:ac:94:fd:1f:e0:a3:48:6d")

    @responses.activate
    def test_get_all_domains(self):
        data = self.load_from_file('domains/all.json')

        url = self.base_url + 'domains/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        domains = self.manager.get_all_domains()
        self.assertEqual(len(domains), 1)

        # Test the few things we can assume about a random domain.
        domain = domains[0]
        self.assertEqual(domain.token, self.token)
        self.assertEqual(domain.name, "example.com")
        self.assertEqual(domain.zone_file, "Example zone file text...")
        self.assertEqual(domain.ttl, 1800)


if __name__ == '__main__':
    unittest.main()
