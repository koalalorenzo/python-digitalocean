import os
import re
import unittest
import responses

import digitalocean

class TestDroplet(unittest.TestCase):

    def load_from_file(self, json_file):
        cwd = os.path.dirname(__file__)
        with open(os.path.join(cwd, 'data/%s' % json_file), 'r') as f:
            return f.read()

    def setUp(self):
        self.base_url = "https://api.digitalocean.com/v2/"
        self.actions_url = self.base_url + "droplets/12345/actions/"
        self.token = "afaketokenthatwillworksincewemockthings"
        self.droplet = digitalocean.Droplet(id='12345', token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('droplets/single.json')

        responses.add(responses.GET, self.base_url + "droplets/12345",
                      body=data,
                      status=200,
                      content_type='application/json')

        droplet = digitalocean.Droplet(id='12345', token=self.token)
        d = droplet.load()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "droplets/12345")
        self.assertEqual(d.id, 12345)
        self.assertEqual(d.name, "example.com")
        self.assertEqual(d.memory, 512)
        self.assertEqual(d.vcpus, 1)
        self.assertEqual(d.disk, 20)
        self.assertEqual(d.region['slug'], "nyc3")
        self.assertEqual(d.status, "active")
        self.assertEqual(d.image['slug'], "ubuntu-14-04-x64")
        self.assertEqual(d.size_slug, '512mb')
        self.assertEqual(d.created_at, "2014-11-14T16:36:31Z")
        self.assertEqual(d.ip_address, "104.131.186.241")
        self.assertEqual(d.ip_v6_address,
                         "2604:A880:0800:0010:0000:0000:031D:2001")
        self.assertEqual(d.kernel['id'], 2233)
        self.assertEqual(d.features, ["ipv6", "virtio"])

    @responses.activate
    def test_power_off(self):
        data = self.load_from_file('droplet_actions/power_off.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.power_off()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=power_off")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "power_off")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_power_on(self):
        data = self.load_from_file('droplet_actions/power_on.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.power_on()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=power_on")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "power_on")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_shutdown(self):
        data = self.load_from_file('droplet_actions/shutdown.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.shutdown()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=shutdown")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "shutdown")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_reboot(self):
        data = self.load_from_file('droplet_actions/reboot.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.reboot()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=reboot")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "reboot")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_power_cycle(self):
        data = self.load_from_file('droplet_actions/power_cycle.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.power_cycle()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=power_cycle")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "power_cycle")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_reset_root_password(self):
        data = self.load_from_file('droplet_actions/password_reset.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.reset_root_password()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=password_reset")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "password_reset")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_take_snapshot(self):
        data = self.load_from_file('droplet_actions/snapshot.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.take_snapshot("New Snapshot")

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=snapshot&name=New+Snapshot")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "snapshot")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_resize(self):
        data = self.load_from_file('droplet_actions/resize.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.resize("64gb")

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=resize&size=64gb")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "resize")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_restore(self):
        data = self.load_from_file('droplet_actions/restore.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.restore(image_id=78945)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?image=78945&type=restore")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "restore")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_rebuild_passing_image(self):
        """
        Test rebuilding an droplet from a provided image id.
        """
        data = self.load_from_file('droplet_actions/rebuild.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.rebuild(image_id=78945)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?image=78945&type=rebuild")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "rebuild")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_rebuild_not_passing_image(self):
        """
        Test rebuilding an droplet from its original parent image id.
        """
        data = self.load_from_file('droplet_actions/rebuild.json')
        droplet_data = self.load_from_file('droplets/single.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')
        responses.add(responses.GET, self.base_url + "droplets/12345",
                      body=droplet_data,
                      status=200,
                      content_type='application/json')

        droplet = digitalocean.Droplet(id='12345', token=self.token)
        d = droplet.load()

        response = d.rebuild()

        self.assertEqual(responses.calls[1].request.url,
                         self.actions_url + "?image=6918990&type=rebuild")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "rebuild")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_disable_backups(self):
        data = self.load_from_file('droplet_actions/disable_backups.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.disable_backups()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=disable_backups")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "disable_backups")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_destroy(self):
        responses.add(responses.DELETE, self.base_url + "droplets/12345",
                      status=204,
                      content_type='application/json')

        response = self.droplet.destroy()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "droplets/12345")

    @responses.activate
    def test_rename(self):
        data = self.load_from_file('droplet_actions/rename.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.rename(name="New Name")

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=rename&name=New+Name")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "rename")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_enable_private_networking(self):
        data = self.load_from_file('droplet_actions/enable_private_networking.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.enable_private_networking()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=enable_private_networking")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "enable_private_networking")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_enable_ipv6(self):
        data = self.load_from_file('droplet_actions/enable_ipv6.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.enable_ipv6()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=enable_ipv6")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "enable_ipv6")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    def test_change_kernel_exception(self):

        with self.assertRaises(Exception) as error:
            self.droplet.change_kernel(kernel=123)

        exception = error.exception
        self.assertEqual(exception.message, 'Use Kernel object')

    @responses.activate
    def test_change_kernel(self):
        data = self.load_from_file('droplet_actions/change_kernel.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.change_kernel(digitalocean.Kernel(id=123))

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?kernel=123&type=change_kernel")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "change_kernel")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_create_no_keys(self):
        data = self.load_from_file('droplet_actions/create.json')

        responses.add(responses.POST, self.base_url + "droplets",
                      body=data,
                      status=202,
                      content_type='application/json')

        droplet = digitalocean.Droplet(name="example.com",
                                       size_slug="512mb",
                                       image="ubuntu-14-04-x64",
                                       region="nyc3",
                                       backups=True,
                                       ipv6=True,
                                       private_networking=True,
                                       user_data="Some user data.",
                                       token=self.token)
        response = droplet.create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + \
                         "droplets?name=example.com&region=nyc3&user_data=Some+user+data.&ipv6=True&private_networking=True&backups=True&image=ubuntu-14-04-x64&size=512mb")
        self.assertEqual(droplet.id, 3164494)
        self.assertEqual(droplet.action_ids, [36805096])