import unittest
import os

import digitalocean

class TestManager(unittest.TestCase):

    def setUp(self):
        self.token = os.environ.get('DO_TOKEN', None)
        self.manager = digitalocean.Manager(token=self.token)

    def test_auth_fail(self):
        bad_token = digitalocean.Manager(token='afaketokenthatwillnotwork')

        with self.assertRaises(Exception) as error:
            bad_token.get_all_regions()

        exception = error.exception
        self.assertEqual(exception.message, 'Unable to authenticate you.')

    def test_get_all_regions(self):
        all_regions = self.manager.get_all_regions()
        self.assertEqual(len(all_regions), 8)

        first_region = all_regions[0]
        self.assertEqual(first_region.token, self.token)
        self.assertEqual(first_region.name, 'New York 1')
        self.assertEqual(first_region.slug, 'nyc1')
        self.assertItemsEqual(first_region.sizes,
            [u'512mb', u'1gb', u'2gb', u'4gb', u'8gb',
             u'16gb', u'32gb', u'48gb', u'64gb'])
        self.assertItemsEqual(first_region.features, [u'virtio', u'backups'])

    def test_get_all_sizes(self):
        all_sizes = self.manager.get_all_sizes()
        self.assertEqual(len(all_sizes), 9)

        first_size = all_sizes[0]
        self.assertEqual(first_size.token, self.token)
        self.assertEqual(first_size.slug, '512mb')
        self.assertEqual(first_size.memory, 512)
        self.assertEqual(first_size.disk, 20)
        self.assertEqual(first_size.price_hourly, 0.00744)
        self.assertEqual(first_size.price_monthly, 5.0)
        self.assertEqual(first_size.transfer, 1)
        self.assertEqual(first_size.transfer, 1)
        self.assertItemsEqual(first_size.regions,
            [u'nyc1', u'sgp1', u'ams1', u'ams2',
            u'sfo1', u'nyc2', u'lon1', u'nyc3'])

    def test_get_all_images(self):
        all_images = self.manager.get_all_images()

        # The order of images is not predictable. So find a certain one.
        for image in all_images:
            if image.slug == 'ubuntu-14-04-x64': 
                ubuntu_trusty_64 = image
                break
        self.assertEqual(ubuntu_trusty_64.token, self.token)
        self.assertEqual(ubuntu_trusty_64.name, 'Ubuntu 14.04 x64')
        self.assertTrue(ubuntu_trusty_64.public)
        self.assertEqual(ubuntu_trusty_64.distribution, 'Ubuntu')
        self.assertItemsEqual(ubuntu_trusty_64.regions,
            [u'nyc1', u'sgp1', u'ams1', u'ams2',
            u'sfo1', u'nyc2', u'lon1', u'nyc3'])
        self.assertIsInstance(ubuntu_trusty_64.id, int)
        self.assertIsNotNone(ubuntu_trusty_64.created_at)

    def test_get_global_images(self):
        global_images = self.manager.get_global_images()
        self.assertEqual(len(global_images), 33)

        # The order of images is not predictable. So find a certain one.
        for image in global_images:
            if image.slug == 'ubuntu-14-04-x64': 
                ubuntu_trusty_64 = image
                break
        self.assertEqual(ubuntu_trusty_64.token, self.token)
        self.assertEqual(ubuntu_trusty_64.name, 'Ubuntu 14.04 x64')
        self.assertTrue(ubuntu_trusty_64.public)
        self.assertEqual(ubuntu_trusty_64.distribution, 'Ubuntu')
        self.assertItemsEqual(ubuntu_trusty_64.regions,
            [u'nyc1', u'sgp1', u'ams1', u'ams2',
            u'sfo1', u'nyc2', u'lon1', u'nyc3'])
        self.assertIsInstance(ubuntu_trusty_64.id, int)
        self.assertIsNotNone(ubuntu_trusty_64.created_at)

    def test_get_my_images(self):
        my_images = self.manager.get_my_images()

        # Test the few things we can assume about a private image
        first_image = my_images[0]
        self.assertEqual(first_image.token, self.token)
        self.assertFalse(first_image.public)
        self.assertIsNone(first_image.slug)
        self.assertIsInstance(first_image.name, unicode)
        self.assertIsInstance(first_image.id, int)
        self.assertIsInstance(first_image.distribution, unicode)
        self.assertIsNotNone(first_image.created_at)

    def test_get_all_droplets(self):
        droplets = self.manager.get_all_droplets()

        # Test the few things we can assume a random droplet.
        first_droplet = droplets[0]
        self.assertEqual(first_droplet.token, self.token)
        self.assertIsInstance(first_droplet.id, int)
        self.assertIsInstance(first_droplet.name, unicode)
        self.assertIsInstance(first_droplet.memory, int)
        self.assertIsInstance(first_droplet.vcpus, int)
        self.assertIsInstance(first_droplet.disk, int)
        self.assertIsInstance(first_droplet.region, dict)
        self.assertIsInstance(first_droplet.status, unicode)
        self.assertIsInstance(first_droplet.image, dict)
        self.assertIsInstance(first_droplet.size, dict)
        self.assertIsNotNone(first_droplet.locked)
        self.assertIsNotNone(first_droplet.created_at)
        self.assertIsInstance(first_droplet.networks, dict)
        self.assertIsInstance(first_droplet.kernel, dict)
        self.assertIsInstance(first_droplet.action_ids, list)
        self.assertIsInstance(first_droplet.features, list)

    def test_get_all_sshkeys(self):
        ssh_keys = self.manager.get_all_sshkeys()

        # Test the few things we can assume about a random ssh key.
        first_key = ssh_keys[0]
        self.assertEqual(first_key.token, self.token)
        self.assertIsInstance(first_key.name, unicode)
        self.assertIsInstance(first_key.id, int)
        self.assertIsInstance(first_key.public_key, unicode)
        self.assertIsInstance(first_key.fingerprint, unicode)

    def test_get_all_domains(self):
        domains = self.manager.get_all_domains()

        # Test the few things we can assume about a random domain.
        first_domain = domains[0]
        self.assertEqual(first_domain.token, self.token)
        self.assertIsInstance(first_domain.name, unicode)
        self.assertIsInstance(first_domain.zone_file, unicode)
        self.assertIsInstance(first_domain.ttl, int)


if __name__ == '__main__':
    unittest.main()
