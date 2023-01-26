import unittest
import responses
import digitalocean
import json

from .BaseTest import BaseTest


class TestFirewall(BaseTest):

    @responses.activate
    def setUp(self):
        super(TestFirewall, self).setUp()

        data = self.load_from_file('firewalls/single.json')

        url = self.base_url + "firewalls/12345"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.firewall = digitalocean.Firewall(id=12345, token=self.token).load()

    @responses.activate
    def test_load(self):
        data = self.load_from_file('firewalls/single.json')

        url = self.base_url + "firewalls/12345"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        firewall = digitalocean.Firewall(id=12345, token=self.token)
        f = firewall.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(f.id, 12345)
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
    def test_add_droplets(self):
        data = self.load_from_file('firewalls/droplets.json')

        url = self.base_url + "firewalls/12345/droplets"
        responses.add(responses.POST, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        droplet_id = json.loads(data)["droplet_ids"][0]
        self.firewall.add_droplets([droplet_id])

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_remove_droplets(self):
        data = self.load_from_file('firewalls/droplets.json')

        url = self.base_url + "firewalls/12345/droplets"
        responses.add(responses.DELETE,
                      url,
                      body=data,
                      status=204,
                      content_type='application/json')

        droplet_id = json.loads(data)["droplet_ids"][0]
        self.firewall.remove_droplets([droplet_id])

        self.assertEqual(responses.calls[0].request.url, url)    

    @responses.activate
    def test_add_tags(self):
        data = self.load_from_file('firewalls/tags.json')

        url = self.base_url + "firewalls/12345/tags"
        responses.add(responses.POST, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        tag = json.loads(data)["tags"][0]
        self.firewall.add_tags([tag])

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_remove_tags(self):
        data = self.load_from_file('firewalls/tags.json')

        url = self.base_url + "firewalls/12345/tags"
        responses.add(responses.DELETE, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        tag = json.loads(data)["tags"][0]
        self.firewall.remove_tags([tag])

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_add_inbound(self):
        data = self.load_from_file('firewalls/rules.json')

        url = self.base_url + "firewalls/12345/rules"
        responses.add(responses.POST, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        rule = json.loads(data)["rules"][0]
        self.firewall.add_inbound([rule])

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_add_outbound(self):
        data = self.load_from_file('firewalls/rules.json')

        url = self.base_url + "firewalls/12345/rules"
        responses.add(responses.POST, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        rule = json.loads(data)["rules"][0]
        self.firewall.add_outbound([rule])

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_remove_inbound(self):
        data = self.load_from_file('firewalls/rules.json')

        url = self.base_url + "firewalls/12345/rules"
        responses.add(responses.DELETE, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        rule = json.loads(data)["rules"][0]
        self.firewall.remove_inbound([rule])

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_remove_outbound(self):
        data = self.load_from_file('firewalls/rules.json')

        url = self.base_url + "firewalls/12345/rules"
        responses.add(responses.DELETE, url,
                      body=data,
                      status=204,
                      content_type='application/json')

        rule = json.loads(data)["rules"][0]
        self.firewall.remove_outbound([rule])

        self.assertEqual(responses.calls[0].request.url, url)

if __name__ == '__main__':
    unittest.main()
