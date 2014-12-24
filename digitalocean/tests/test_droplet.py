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

    @responses.activate
    def setUp(self):
        self.base_url = "https://api.digitalocean.com/v2/"
        self.actions_url = self.base_url + "droplets/12345/actions/"
        self.token = "afaketokenthatwillworksincewemockthings"

        data = self.load_from_file('droplets/single.json')
        responses.add(responses.GET, self.base_url + "droplets/12345",
                      body=data,
                      status=200,
                      content_type='application/json')
        self.droplet = digitalocean.Droplet(id='12345', token=self.token).load()

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
    def test_power_off_action(self):
        data = self.load_from_file('droplet_actions/power_off.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.power_off(False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=power_off")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "power_off")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_power_on_action(self):
        data = self.load_from_file('droplet_actions/power_on.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.power_on(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=power_on")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "power_on")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_shutdown_action(self):
        data = self.load_from_file('droplet_actions/shutdown.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.shutdown(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=shutdown")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "shutdown")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_reboot_action(self):
        data = self.load_from_file('droplet_actions/reboot.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.reboot(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=reboot")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "reboot")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")


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
    def test_power_cycle_action(self):
        data = self.load_from_file('droplet_actions/power_cycle.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.power_cycle(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=power_cycle")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "power_cycle")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_reset_root_password_action(self):
        data = self.load_from_file('droplet_actions/password_reset.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.reset_root_password(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=password_reset")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "password_reset")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_take_snapshot_action(self):
        data = self.load_from_file('droplet_actions/snapshot.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.take_snapshot("New Snapshot", return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=snapshot&name=New+Snapshot")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "snapshot")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_resize_action(self):
        data = self.load_from_file('droplet_actions/resize.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.resize("64gb", False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=resize&size=64gb")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "resize")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_restore_action(self):
        data = self.load_from_file('droplet_actions/restore.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.restore(image_id=78945, return_dict = False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?image=78945&type=restore")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "restore")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_rebuild_passing_image_action(self):
        """
        Test rebuilding an droplet from a provided image id.
        """
        data = self.load_from_file('droplet_actions/rebuild.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.rebuild(image_id=78945, return_dict = False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?image=78945&type=rebuild")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "rebuild")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

    @responses.activate
    def test_rebuild_not_passing_image(self):
        """
        Test rebuilding an droplet from its original parent image id.
        """
        data = self.load_from_file('droplet_actions/rebuild.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.rebuild()

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?image=6918990&type=rebuild")
        self.assertEqual(response['action']['id'], 54321)
        self.assertEqual(response['action']['status'], "in-progress")
        self.assertEqual(response['action']['type'], "rebuild")
        self.assertEqual(response['action']['resource_id'], 12345)
        self.assertEqual(response['action']['resource_type'], "droplet")

    @responses.activate
    def test_rebuild_not_passing_image_action(self):
        """
        Test rebuilding an droplet from its original parent image id.
        """
        data = self.load_from_file('droplet_actions/rebuild.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.rebuild(return_dict = False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?image=6918990&type=rebuild")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "rebuild")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_disable_backups_action(self):
        data = self.load_from_file('droplet_actions/disable_backups.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.disable_backups(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=disable_backups")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "disable_backups")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_rename_action(self):
        data = self.load_from_file('droplet_actions/rename.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.rename(name="New Name", return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=rename&name=New+Name")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "rename")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_enable_private_networking_action(self):
        data = self.load_from_file('droplet_actions/enable_private_networking.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.enable_private_networking(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=enable_private_networking")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "enable_private_networking")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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

    @responses.activate
    def test_enable_ipv6_action(self):
        data = self.load_from_file('droplet_actions/enable_ipv6.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.enable_ipv6(return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?type=enable_ipv6")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "enable_ipv6")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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
    def test_change_kernel_action(self):
        data = self.load_from_file('droplet_actions/change_kernel.json')

        responses.add(responses.POST, self.actions_url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.droplet.change_kernel(digitalocean.Kernel(id=123),
                return_dict=False)

        self.assertEqual(responses.calls[0].request.url,
                         self.actions_url + "?kernel=123&type=change_kernel")
        self.assertEqual(response.id, 54321)
        self.assertEqual(response.status, "in-progress")
        self.assertEqual(response.type, "change_kernel")
        self.assertEqual(response.resource_id, 12345)
        self.assertEqual(response.resource_type, "droplet")

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

    @responses.activate
    def test_get_actions(self):
        data = self.load_from_file('actions/multi.json')
        create = self.load_from_file('actions/create_completed.json')
        ipv6 = self.load_from_file('actions/ipv6_completed.json')

        responses.add(responses.GET, self.actions_url,
                      body=data,
                      status=200,
                      content_type='application/json')
        responses.add(responses.GET, self.actions_url + "39388122",
                      body=create,
                      status=200,
                      content_type='application/json')
        responses.add(responses.GET, self.actions_url + "39290099",
                      body=ipv6,
                      status=200,
                      content_type='application/json')

        actions = self.droplet.get_actions()

        self.assertEqual(len(actions), 2)
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(responses.calls[0].request.url, self.actions_url)
        self.assertEqual(responses.calls[1].request.url,
                         self.actions_url + "39388122")
        self.assertEqual(responses.calls[2].request.url,
                         self.actions_url + "39290099")
        self.assertEqual(actions[0].id, 39290099)
        self.assertEqual(actions[0].type, "create")
        self.assertEqual(actions[0].status, "completed")
        self.assertEqual(actions[1].id, 39388122)
        self.assertEqual(actions[1].type, "enable_ipv6")
        self.assertEqual(actions[1].status, "completed")

    @responses.activate
    def test_get_action(self):
        data = self.load_from_file('actions/create_completed.json')

        responses.add(responses.GET, self.base_url + "actions/39388122",
                      body=data,
                      status=200,
                      content_type='application/json')

        action = self.droplet.get_action(39388122)

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "actions/39388122")
        self.assertEqual(action.id, 39290099)
        self.assertEqual(action.type, "create")
        self.assertEqual(action.status, "completed")

    def test_get_snapshots(self):
        snapshots = self.droplet.get_snapshots()

        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[0].id, 7938206)

    @responses.activate
    def test_get_kernel_available_no_pages(self):
        data = self.load_from_file('kernels/list.json')

        responses.add(responses.GET, self.base_url + "droplets/12345/kernels/",
                      body=data,
                      status=200,
                      content_type='application/json')

        kernels = self.droplet.get_kernel_available()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "droplets/12345/kernels/")
        self.assertEqual(len(kernels), 2)
        self.assertEqual(kernels[0].id, 61833229)
        self.assertEqual(kernels[0].name,
                         "Ubuntu 14.04 x32 vmlinuz-3.13.0-24-generic")

    @responses.activate
    def test_get_kernel_available_with_pages(self):
        one = self.load_from_file('kernels/page_one.json')
        two = self.load_from_file('kernels/page_two.json')

        responses.add(responses.GET, self.base_url + "droplets/12345/kernels/",
                      body=one,
                      status=200,
                      content_type='application/json')
        responses.add(responses.GET,
                      self.base_url + "droplets/12345/kernels?page=2",
                      body=two,
                      status=200,
                      content_type='application/json',
                      match_querystring=True)

        kernels = self.droplet.get_kernel_available()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "droplets/12345/kernels/")
        self.assertEqual(responses.calls[1].request.url,
                         self.base_url + "droplets/12345/kernels?page=2")
        self.assertEqual(len(kernels), 3)
        self.assertEqual(kernels[0].id, 61833229)
        self.assertEqual(kernels[0].name,
                         "Ubuntu 14.04 x32 vmlinuz-3.13.0-24-generic")
        self.assertEqual(kernels[2].id, 231)
        self.assertEqual(kernels[2].name,
                         "Ubuntu 14.04 x64 vmlinuz-3.13.0-32-generic")
