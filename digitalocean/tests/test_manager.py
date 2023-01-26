import json
import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestManager(BaseTest):

    def setUp(self):
        super(TestManager, self).setUp()
        self.manager = digitalocean.Manager(token=self.token)
        self.image = digitalocean.Image(
            id=449676856, slug='testslug', token=self.token
        )

    @responses.activate
    def test_get_account(self):
        data = self.load_from_file('account/account.json')

        url = self.base_url + 'account/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        acct = self.manager.get_account()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(acct.token, self.token)
        self.assertEqual(acct.email, 'web@digitalocean.com')
        self.assertEqual(acct.droplet_limit, 25)
        self.assertEqual(acct.email_verified, True)
        self.assertEqual(acct.status, "active")

    @responses.activate
    def test_get_balance(self):
        data = self.load_from_file('balance/balance.json')

        url = self.base_url + 'customers/my/balance'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        balance = self.manager.get_balance()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(balance.token, balance.token)
        self.assertEqual(balance.month_to_date_balance, '23.44')
        self.assertEqual(balance.account_balance, '12.23')
        self.assertEqual(balance.month_to_date_usage, '11.21')
        self.assertEqual(balance.generated_at, '2019-07-09T15:01:12Z')

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
        self.assertEqual(str(exception), 'Unable to authenticate you.')

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
        self.assertEqual(droplet.backups, True)
        self.assertEqual(droplet.ipv6, True)
        self.assertEqual(droplet.private_networking, False)
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
    def test_get_droplets_by_tag(self):
        data = self.load_from_file('droplets/bytag.json')

        url = self.base_url + "droplets"
        responses.add(responses.GET,
                      url + "/",
                      body=data,
                      status=200,
                      content_type='application/json')

        # The next pages don"t use trailing slashes. Return an empty result
        # to prevent an infinite loop
        responses.add(responses.GET,
                      url,
                      body="{}",
                      status=200,
                      content_type="application/json")

        manager = digitalocean.Manager(token=self.token)
        droplets = manager.get_all_droplets(tag_name="awesome")

        droplet = droplets[0]
        self.assertEqual(droplet.token, self.token)
        self.assertEqual(droplet.id, 3164444)
        self.assertEqual(droplet.name, "example.com")
        self.assertEqual(droplet.memory, 512)
        self.assertEqual(droplet.vcpus, 1)
        self.assertEqual(droplet.disk, 20)
        self.assertEqual(droplet.backups, True)
        self.assertEqual(droplet.ipv6, True)
        self.assertEqual(droplet.private_networking, False)
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
        self.assertEqual(droplet.tags, ["awesome"])

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
        self.assertEqual(region.sizes, ["1gb", "512mb"])
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
    def test_get_image(self):
        """Test get image by id."""
        data = self.load_from_file('images/single.json')
        url = "{}images/{}".format(self.base_url, self.image.id)

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.image.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.image.id, 449676856)
        self.assertEqual(self.image.slug, 'testslug')
        self.assertEqual(self.image.name, 'My Snapshot')

    @responses.activate
    def test_get_image_by_slug(self):
        """Test get image by slug."""
        data = self.load_from_file('images/single.json')
        url = "{}images/{}".format(self.base_url, self.image.slug)
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.image.load(use_slug=True)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.image.id, 449676856)
        self.assertEqual(self.image.slug, 'testslug')
        self.assertEqual(self.image.name, 'My Snapshot')

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
        data = self.load_from_file('images/private.json')

        url = self.base_url + 'images/'
        responses.add(responses.GET,
                      url,
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
        self.assert_url_query_equal(
            responses.calls[0].request.url,
            'https://api.digitalocean.com/v2/images/?private=true&per_page=200'
        )

    @responses.activate
    def test_get_distro_images(self):
        data = self.load_from_file('images/distro.json')

        url = self.base_url + 'images/'
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        distro_images = self.manager.get_distro_images()
        self.assertEqual(len(distro_images), 2)

        image = distro_images[0]
        self.assertEqual(image.token, self.token)
        self.assertEqual(image.id, 119192817)
        self.assertEqual(image.name, '14.04 x64')
        self.assertTrue(image.public)
        self.assertEqual(image.slug, "ubuntu-14-04-x64")
        self.assertEqual(image.distribution, 'Ubuntu')
        self.assert_url_query_equal(responses.calls[0].request.url,
                                    'https://api.digitalocean.com/v2/images/?type=distribution&per_page=200')

    @responses.activate
    def test_get_app_images(self):
        data = self.load_from_file('images/app.json')

        url = self.base_url + 'images/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        app_images = self.manager.get_app_images()
        self.assertEqual(len(app_images), 2)

        image = app_images[0]
        self.assertEqual(image.token, self.token)
        self.assertEqual(image.id, 11146864)
        self.assertEqual(image.name, 'MEAN on 14.04')
        self.assertTrue(image.public)
        self.assertEqual(image.slug, "mean")
        self.assertEqual(image.distribution, 'Ubuntu')
        self.assert_url_query_equal(responses.calls[0].request.url,
                                    'https://api.digitalocean.com/v2/images/?type=application&per_page=200')

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
    def test_post_new_ssh_key(self):
        data = self.load_from_file('keys/newly_posted.json')

        url = self.base_url + 'account/keys/'
        responses.add(responses.POST, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        params = {'public_key': 'AAAAkey', 'name': 'new_key'}
        ssh_key = self.manager.get_data(url='account/keys/',
                                        type='POST',
                                        params=params)

        key = ssh_key['ssh_key']
        self.assertEqual(key['id'], 1234)
        self.assertEqual(key['fingerprint'], 'ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff')
        self.assertEqual(key['public_key'], 'AAAAkey')
        self.assertEqual(key['name'], 'new_key')

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

    @responses.activate
    def test_get_all_floating_ips(self):
        data = self.load_from_file('floatingip/list.json')

        url = self.base_url + "floating_ips"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        fips = self.manager.get_all_floating_ips()

        self.assertEqual(fips[0].ip, "45.55.96.47")
        self.assertEqual(fips[0].region['slug'], 'nyc3')

    @responses.activate
    def test_get_all_load_balancers(self):
        data = self.load_from_file('loadbalancer/all.json')

        url = self.base_url + "load_balancers"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        lbs = self.manager.get_all_load_balancers()
        resp_rules = lbs[0].forwarding_rules[0]

        self.assertEqual(lbs[0].id, '4de7ac8b-495b-4884-9a69-1050c6793cd6')
        self.assertEqual(lbs[0].algorithm, 'round_robin')
        self.assertEqual(lbs[0].ip, '104.131.186.241')
        self.assertEqual(lbs[0].name, 'example-lb-01')
        self.assertEqual(len(lbs[0].forwarding_rules), 2)
        self.assertEqual(resp_rules.entry_protocol, 'http')
        self.assertEqual(resp_rules.entry_port, 80)
        self.assertEqual(resp_rules.target_protocol, 'http')
        self.assertEqual(resp_rules.target_port, 80)
        self.assertEqual(resp_rules.tls_passthrough, False)
        self.assertEqual(lbs[0].health_check.protocol, 'http')
        self.assertEqual(lbs[0].health_check.port, 80)
        self.assertEqual(lbs[0].sticky_sessions.type, 'none')
        self.assertEqual(lbs[0].tag, '')
        self.assertEqual(lbs[0].droplet_ids, [3164444, 3164445])

    @responses.activate
    def test_get_all_certificates(self):
        data = self.load_from_file('certificate/list.json')

        url = self.base_url + "certificates"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        certs = self.manager.get_all_certificates()

        self.assertEqual(certs[0].id, '892071a0-bb95-49bc-8021-3afd67a210bf')
        self.assertEqual(certs[0].name, 'web-cert-01')
        self.assertEqual(certs[0].sha1_fingerprint,
            'dfcc9f57d86bf58e321c2c6c31c7a971be244ac7')
        self.assertEqual(certs[0].not_after, '2017-02-22T00:23:00Z')
        self.assertEqual(certs[0].created_at, '2017-02-08T16:02:37Z')
        self.assertEqual(certs[0].type, 'custom')
        self.assertEqual(certs[0].state, 'verified')

        self.assertEqual(certs[1].id, 'ba9b9c18-6c59-46c2-99df-70da170a42ba')
        self.assertEqual(certs[1].name, 'web-cert-02')
        self.assertEqual(certs[1].sha1_fingerprint,
            '479c82b5c63cb6d3e6fac4624d58a33b267e166c')
        self.assertEqual(certs[1].not_after, '2018-06-07T17:44:12Z')
        self.assertEqual(certs[1].created_at, '2018-03-09T18:44:11Z')
        self.assertEqual(certs[1].type, 'lets_encrypt')
        self.assertEqual(certs[1].state, 'pending')

    @responses.activate
    def test_get_all_volumes(self):
        data = self.load_from_file('volumes/all.json')

        url = self.base_url + "volumes"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        volumes = self.manager.get_all_volumes()

        self.assertEqual(volumes[0].id, "506f78a4-e098-11e5-ad9f-000f53306ae1")
        self.assertEqual(volumes[0].region['slug'], 'nyc1')
        self.assertEqual(volumes[0].filesystem_type, "ext4")
        self.assertEqual(len(volumes), 2)

    @responses.activate
    def test_get_per_region_volumes(self):
        data = json.loads(self.load_from_file('volumes/all.json'))
        data["volumes"] = [
            volume for volume in data["volumes"]
            if volume["region"]["slug"] == "nyc1"]

        url = self.base_url + "volumes?region=nyc1&per_page=200"
        responses.add(responses.GET, url,
                      match_querystring=True,
                      body=json.dumps(data),
                      status=200,
                      content_type='application/json')
        volumes = self.manager.get_all_volumes("nyc1")

        self.assertEqual(volumes[0].id, "506f78a4-e098-11e5-ad9f-000f53306ae1")
        self.assertEqual(volumes[0].region['slug'], 'nyc1')
        self.assertEqual(len(volumes), 1)

    @responses.activate
    def test_get_named_volumes(self):
        data = json.loads(self.load_from_file('volumes/all.json'))
        data["volumes"] = [
            volume for volume in data["volumes"]
            if volume["name"] == "another-example"]

        url = self.base_url + "volumes?name=another-example&per_page=200"
        responses.add(responses.GET, url,
                      match_querystring=True,
                      body=json.dumps(data),
                      status=200,
                      content_type='application/json')
        volumes = self.manager.get_all_volumes(name="another-example")

        self.assertEqual(volumes[0].id, "2d2967ff-491d-11e6-860c-000f53315870")
        self.assertEqual(volumes[0].name, 'another-example')
        self.assertEqual(len(volumes), 1)

    @responses.activate
    def test_get_all_tags(self):
        data = self.load_from_file('tags/all.json')

        url = self.base_url + 'tags'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_tags = self.manager.get_all_tags()

        self.assertEqual(len(all_tags), 1)
        self.assertEqual(all_tags[0].name, 'test')
        self.assertEqual(all_tags[0].resources['droplets']['count'], 0)

    @responses.activate
    def test_get_all_snapshots(self):
        data = self.load_from_file('snapshots/all.json')

        url = self.base_url + 'snapshots/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_snapshots = self.manager.get_all_snapshots()

        self.assertEqual(len(all_snapshots), 1)
        self.assertEqual(all_snapshots[0].name, 'test')
        self.assertEqual(all_snapshots[0].id, 6372321)
        self.assertEqual(all_snapshots[0].size_gigabytes, 1.42)
        self.assertEqual(all_snapshots[0].resource_type, 'droplet')
        self.assertEqual(len(all_snapshots[0].regions), 11)

    @responses.activate
    def test_get_droplet_snapshots(self):
        data = self.load_from_file('snapshots/droplets.json')

        url = self.base_url + 'snapshots?resource_type=droplet&per_page=200'
        responses.add(responses.GET, url,
                      match_querystring=True,
                      body=data,
                      status=200,
                      content_type='application/json')

        droplet_snapshots = self.manager.get_droplet_snapshots()

        self.assertEqual(len(droplet_snapshots), 1)
        self.assertEqual(droplet_snapshots[0].name, 'droplet-test')
        self.assertEqual(droplet_snapshots[0].id, 19602538)
        self.assertEqual(droplet_snapshots[0].min_disk_size, 20)
        self.assertEqual(droplet_snapshots[0].size_gigabytes, 0.31)
        self.assertEqual(droplet_snapshots[0].resource_type, 'droplet')
        self.assertEqual(len(droplet_snapshots[0].regions), 12)

    @responses.activate
    def test_get_volume_snapshots(self):
        data = self.load_from_file('snapshots/volumes.json')

        url = self.base_url + 'snapshots?resource_type=volume&per_page=200'
        responses.add(responses.GET, url,
                      match_querystring=True,
                      body=data,
                      status=200,
                      content_type='application/json')

        volume_snapshots = self.manager.get_volume_snapshots()

        self.assertEqual(len(volume_snapshots), 1)
        self.assertEqual(volume_snapshots[0].name, 'volume-test')
        self.assertEqual(
            volume_snapshots[0].id, '4f60fc64-85d1-11e6-a004-000f53315871'
        )
        self.assertEqual(volume_snapshots[0].min_disk_size, 10)
        self.assertEqual(volume_snapshots[0].size_gigabytes, 0)
        self.assertEqual(volume_snapshots[0].resource_type, 'volume')
        self.assertEqual(len(volume_snapshots[0].regions), 1)

    @responses.activate
    def test_get_all_projects(self):
        data = self.load_from_file('projects/all_projects_list.json')
        url = self.base_url + 'projects'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        all_projects = self.manager.get_all_projects()

        self.assertEqual(len(all_projects), 1)
        self.assertEqual(all_projects[0].id, "4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")
        self.assertEqual(all_projects[0].owner_uuid, "99525febec065ca37b2ffe4f852fd2b2581895e7")
        self.assertEqual(all_projects[0].owner_id, 2)
        self.assertEqual(all_projects[0].name, "my-web-api")
        self.assertEqual(all_projects[0].description, "My website API")
        self.assertEqual(all_projects[0].purpose, "Service or API")
        self.assertEqual(all_projects[0].environment, "Production")
        self.assertEqual(all_projects[0].is_default, False)
        self.assertEqual(all_projects[0].created_at, "2018-09-27T20:10:35Z")
        self.assertEqual(all_projects[0].updated_at, "2018-09-27T20:10:35Z")

    @responses.activate
    def test_get_default_project(self):
        data = self.load_from_file('projects/default_project.json')
        url = self.base_url + 'projects' + "/default"
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        default_project = self.manager.get_default_project()

        self.assertEqual(default_project.id, "4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679")
        self.assertEqual(default_project.owner_uuid, "99525febec065ca37b2ffe4f852fd2b2581895e7")
        self.assertEqual(default_project.owner_id, 2)
        self.assertEqual(default_project.name, "my-web-api")
        self.assertEqual(default_project.description, "My website API")
        self.assertEqual(default_project.purpose, "Service or API")
        self.assertEqual(default_project.environment, "Production")
        self.assertEqual(default_project.is_default, True)
        self.assertEqual(default_project.created_at, "2018-09-27T20:10:35Z")
        self.assertEqual(default_project.updated_at, "2018-09-27T20:10:35Z")

    @responses.activate
    def test_get_firewalls(self):
        data = self.load_from_file('firewalls/all.json')

        url = self.base_url + "firewalls"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        firewalls = self.manager.get_all_firewalls()
        f = firewalls[0]

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(f.id, "12345")
        self.assertEqual(f.name, "firewall")
        self.assertEqual(f.status, "succeeded")
        self.assertEqual(f.inbound_rules[0].ports, "80")
        self.assertEqual(f.inbound_rules[0].protocol, "tcp")
        self.assertEqual(f.inbound_rules[0].sources.load_balancer_uids,
                         ["12345"])
        self.assertEqual(f.inbound_rules[0].sources.addresses, [])
        self.assertEqual(f.inbound_rules[0].sources.tags, [])
        self.assertEqual(f.outbound_rules[0].ports, "80")
        self.assertEqual(f.outbound_rules[0].protocol, "tcp")
        self.assertEqual(
            f.outbound_rules[0].destinations.load_balancer_uids, [])
        self.assertEqual(f.outbound_rules[0].destinations.addresses,
                         ["0.0.0.0/0", "::/0"])
        self.assertEqual(f.outbound_rules[0].destinations.tags, [])
        self.assertEqual(f.created_at, "2017-05-23T21:24:00Z")
        self.assertEqual(f.droplet_ids, [12345])
        self.assertEqual(f.tags, [])
        self.assertEqual(f.pending_changes, [])

    @responses.activate
    def test_get_vpc(self):
        data = self.load_from_file('vpcs/single.json')
        vpc_id = "5a4981aa-9653-4bd1-bef5-d6bff52042e4"
        url = self.base_url + 'vpcs/' + vpc_id

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        vpc = self.manager.get_vpc(vpc_id)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(vpc.id, vpc_id)
        self.assertEqual(vpc.name, 'my-new-vpc')
        self.assertEqual(vpc.region, 'nyc1')
        self.assertEqual(vpc.ip_range, '10.10.10.0/24')
        self.assertEqual(vpc.description, '')
        self.assertEqual(vpc.urn, 'do:vpc:5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(vpc.created_at, '2020-03-13T18:48:45Z')
        self.assertEqual(vpc.default, False)

    @responses.activate
    def test_get_all_vpcs(self):
        data = self.load_from_file('vpcs/list.json')

        url = self.base_url + "vpcs"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        vpcs = self.manager.get_all_vpcs()

        self.assertEqual(vpcs[0].id, '5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(vpcs[0].name, 'my-new-vpc')
        self.assertEqual(vpcs[0].created_at, '2020-03-13T19:20:47Z')
        self.assertEqual(vpcs[0].region, 'nyc1')
        self.assertEqual(vpcs[0].description, '')
        self.assertEqual(vpcs[0].urn,
            'do:vpc:5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(vpcs[0].ip_range, '10.10.10.0/24')
        self.assertEqual(vpcs[0].default, False)
        self.assertEqual(vpcs[1].id, 'e0fe0f4d-596a-465e-a902-571ce57b79fa')
        self.assertEqual(vpcs[1].name, 'default-nyc1')
        self.assertEqual(vpcs[1].description, '')
        self.assertEqual(vpcs[1].urn,
            'do:vpc:e0fe0f4d-596a-465e-a902-571ce57b79fa')
        self.assertEqual(vpcs[1].ip_range, '10.102.0.0/20')
        self.assertEqual(vpcs[1].created_at, '2020-03-13T19:29:20Z')
        self.assertEqual(vpcs[1].region, 'nyc1')
        self.assertEqual(vpcs[1].default, True)


if __name__ == '__main__':
    unittest.main()
