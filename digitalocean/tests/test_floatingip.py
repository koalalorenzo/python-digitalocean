import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestFloatingIP(BaseTest):

    def setUp(self):
        super(TestFloatingIP, self).setUp()
        self.fip = digitalocean.FloatingIP(ip='45.55.96.47', token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('floatingip/single.json')

        responses.add(responses.GET,
                      self.base_url + "floating_ips/45.55.96.47",
                      body=data,
                      status=200,
                      content_type='application/json')

        self.fip.load()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "floating_ips/45.55.96.47")
        self.assertEqual(self.fip.ip, "45.55.96.47")
        self.assertEqual(self.fip.region['slug'], 'nyc3')

    @responses.activate
    def test_create(self):
        data = self.load_from_file('floatingip/single.json')

        responses.add(responses.POST,
                      self.base_url + "floating_ips/",
                      body=data,
                      status=201,
                      content_type='application/json')

        fip = digitalocean.FloatingIP(droplet_id=12345,
                                      token=self.token).create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "floating_ips/")
        self.assertEqual(fip.ip, "45.55.96.47")
        self.assertEqual(fip.region['slug'], 'nyc3')

    @responses.activate
    def test_reserve(self):
        data = self.load_from_file('floatingip/single.json')

        responses.add(responses.POST,
                      self.base_url + "floating_ips/",
                      body=data,
                      status=201,
                      content_type='application/json')

        fip = digitalocean.FloatingIP(region_slug='nyc3',
                                      token=self.token).reserve()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "floating_ips/")
        self.assertEqual(fip.ip, "45.55.96.47")
        self.assertEqual(fip.region['slug'], 'nyc3')

    @responses.activate
    def test_destroy(self):
        responses.add(responses.DELETE,
                      self.base_url + "floating_ips/45.55.96.47/",
                      status=204,
                      content_type='application/json')

        self.fip.destroy()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "floating_ips/45.55.96.47/")

    @responses.activate
    def test_assign(self):
        data = self.load_from_file('floatingip/assign.json')

        responses.add(responses.POST,
                      "{}floating_ips/{}/actions/".format(
                        self.base_url, self.fip.ip),
                      body=data,
                      status=201,
                      content_type='application/json')

        res = self.fip.assign(droplet_id=12345)

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "floating_ips/45.55.96.47/actions/")
        self.assertEqual(res['action']['type'], 'assign_ip')
        self.assertEqual(res['action']['status'], 'in-progress')
        self.assertEqual(res['action']['id'], 68212728)

    @responses.activate
    def test_unassign(self):
        data = self.load_from_file('floatingip/unassign.json')

        responses.add(responses.POST,
                      "{}floating_ips/{}/actions/".format(
                        self.base_url, self.fip.ip),
                      body=data,
                      status=201,
                      content_type='application/json')

        res = self.fip.unassign()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "floating_ips/45.55.96.47/actions/")
        self.assertEqual(res['action']['type'], 'unassign_ip')
        self.assertEqual(res['action']['status'], 'in-progress')
        self.assertEqual(res['action']['id'], 68212773)

if __name__ == '__main__':
    unittest.main()
