import json
import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestLoadBalancer(BaseTest):

    def setUp(self):
        super(TestLoadBalancer, self).setUp()
        self.lb_id = '4de7ac8b-495b-4884-9a69-1050c6793cd6'
        self.lb = digitalocean.LoadBalancer(id=self.lb_id, token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('loadbalancer/single.json')
        url = self.base_url + 'load_balancers/' + self.lb_id

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.lb.load()
        rules = self.lb.forwarding_rules

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.lb.id, self.lb_id)
        self.assertEqual(self.lb.region['slug'], 'nyc3')
        self.assertEqual(self.lb.algorithm, 'round_robin')
        self.assertEqual(self.lb.ip, '104.131.186.241')
        self.assertEqual(self.lb.name, 'example-lb-01')
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0].entry_protocol, 'http')
        self.assertEqual(rules[0].entry_port, 80)
        self.assertEqual(rules[0].target_protocol, 'http')
        self.assertEqual(rules[0].target_port, 80)
        self.assertEqual(rules[0].tls_passthrough, False)
        self.assertEqual(self.lb.health_check.protocol, 'http')
        self.assertEqual(self.lb.health_check.port, 80)
        self.assertEqual(self.lb.sticky_sessions.type, 'none')
        self.assertEqual(self.lb.droplet_ids, [3164444, 3164445])

    @responses.activate
    def test_create_ids(self):
        data = self.load_from_file('loadbalancer/single.json')

        url = self.base_url + "load_balancers/"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        rule1 = digitalocean.ForwardingRule(entry_port=80,
                                            entry_protocol='http',
                                            target_port=80,
                                            target_protocol='http')
        rule2 = digitalocean.ForwardingRule(entry_port=443,
                                            entry_protocol='https',
                                            target_port=443,
                                            target_protocol='https',
                                            tls_passthrough=True)
        check = digitalocean.HealthCheck()
        sticky = digitalocean.StickySesions(type='none')
        lb = digitalocean.LoadBalancer(name='example-lb-01', region='nyc3',
                                       algorithm='round_robin',
                                       forwarding_rules=[rule1, rule2],
                                       health_check=check,
                                       sticky_sessions=sticky,
                                       redirect_http_to_https=False,
                                       droplet_ids=[3164444, 3164445],
                                       token=self.token).create()
        resp_rules = lb.forwarding_rules

        self.assert_url_query_equal(responses.calls[0].request.url, url)
        self.assertEqual(lb.id, self.lb_id)
        self.assertEqual(lb.algorithm, 'round_robin')
        self.assertEqual(lb.ip, '104.131.186.241')
        self.assertEqual(lb.name, 'example-lb-01')
        self.assertEqual(len(resp_rules), 2)
        self.assertEqual(resp_rules[0].entry_protocol, 'http')
        self.assertEqual(resp_rules[0].entry_port, 80)
        self.assertEqual(resp_rules[0].target_protocol, 'http')
        self.assertEqual(resp_rules[0].target_port, 80)
        self.assertEqual(resp_rules[0].tls_passthrough, False)
        self.assertEqual(lb.health_check.protocol, 'http')
        self.assertEqual(lb.health_check.port, 80)
        self.assertEqual(lb.sticky_sessions.type, 'none')
        self.assertEqual(lb.droplet_ids, [3164444, 3164445])

    @responses.activate
    def test_create_tag(self):
        data = self.load_from_file('loadbalancer/single_tag.json')

        url = self.base_url + "load_balancers/"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        rule1 = digitalocean.ForwardingRule(entry_port=80,
                                            entry_protocol='http',
                                            target_port=80,
                                            target_protocol='http')
        rule2 = digitalocean.ForwardingRule(entry_port=443,
                                            entry_protocol='https',
                                            target_port=443,
                                            target_protocol='https',
                                            tls_passthrough=True)
        check = digitalocean.HealthCheck()
        sticky = digitalocean.StickySesions(type='none')
        lb = digitalocean.LoadBalancer(name='example-lb-01', region='nyc3',
                                       algorithm='round_robin',
                                       forwarding_rules=[rule1, rule2],
                                       health_check=check,
                                       sticky_sessions=sticky,
                                       redirect_http_to_https=False,
                                       tag='web',
                                       token=self.token).create()
        resp_rules = lb.forwarding_rules

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + 'load_balancers/')
        self.assertEqual(lb.id, '4de2ac7b-495b-4884-9e69-1050d6793cd4')
        self.assertEqual(lb.algorithm, 'round_robin')
        self.assertEqual(lb.ip, '104.131.186.248')
        self.assertEqual(lb.name, 'example-lb-01')
        self.assertEqual(len(resp_rules), 2)
        self.assertEqual(resp_rules[0].entry_protocol, 'http')
        self.assertEqual(resp_rules[0].entry_port, 80)
        self.assertEqual(resp_rules[0].target_protocol, 'http')
        self.assertEqual(resp_rules[0].target_port, 80)
        self.assertEqual(resp_rules[0].tls_passthrough, False)
        self.assertEqual(lb.health_check.protocol, 'http')
        self.assertEqual(lb.health_check.port, 80)
        self.assertEqual(lb.sticky_sessions.type, 'none')
        self.assertEqual(lb.tag, 'web')
        self.assertEqual(lb.droplet_ids, [3164444, 3164445])

    @responses.activate
    def test_create_exception(self):
        data = self.load_from_file('loadbalancer/single_tag.json')

        url = self.base_url + "load_balancers/"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        rule = digitalocean.ForwardingRule(entry_port=80,
                                           entry_protocol='http',
                                           target_port=80,
                                           target_protocol='http')
        check = digitalocean.HealthCheck()
        sticky = digitalocean.StickySesions(type='none')
        lb = digitalocean.LoadBalancer(name='example-lb-01', region='nyc3',
                                       algorithm='round_robin',
                                       forwarding_rules=[rule],
                                       health_check=check,
                                       sticky_sessions=sticky,
                                       redirect_http_to_https=False,
                                       tag='web',
                                       droplet_ids=[123456, 789456],
                                       token=self.token)

        with self.assertRaises(ValueError) as context:
            lb.create()

        self.assertEqual('droplet_ids and tag are mutually exclusive args',
                         str(context.exception))

    @responses.activate
    def test_destroy(self):
        url = '{0}load_balancers/{1}/'.format(self.base_url, self.lb_id)
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        self.lb.destroy()

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_add_droplets(self):
        url = '{0}load_balancers/{1}/droplets/'.format(self.base_url,
                                                       self.lb_id)
        responses.add(responses.POST,
                      url,
                      status=204,
                      content_type='application/json')

        self.lb.add_droplets([12345, 78945])

        body = '{"droplet_ids": [12345, 78945]}'

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(responses.calls[0].request.body, body)

    @responses.activate
    def test_remove_droplets(self):
        url = '{0}load_balancers/{1}/droplets/'.format(self.base_url,
                                                       self.lb_id)
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        self.lb.remove_droplets([12345, 78945])

        body = '{"droplet_ids": [12345, 78945]}'

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(responses.calls[0].request.body, body)

    @responses.activate
    def test_add_forwarding_rules(self):
        url = '{0}load_balancers/{1}/forwarding_rules/'.format(self.base_url,
                                                               self.lb_id)
        responses.add(responses.POST,
                      url,
                      status=204,
                      content_type='application/json')

        rule = digitalocean.ForwardingRule(entry_port=3306,
                                           entry_protocol='tcp',
                                           target_port=3306,
                                           target_protocol='tcp')

        self.lb.add_forwarding_rules([rule])

        req_body = json.loads("""{
  "forwarding_rules": [
    {
      "entry_protocol": "tcp",
      "entry_port": 3306,
      "target_protocol": "tcp",
      "target_port": 3306,
      "certificate_id": "",
      "tls_passthrough": false
    }
  ]
}""")
        body = json.loads(responses.calls[0].request.body)

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(sorted(body.items()), sorted(req_body.items()))

    @responses.activate
    def test_remove_forwarding_rules(self):
        url = '{0}load_balancers/{1}/forwarding_rules/'.format(self.base_url,
                                                               self.lb_id)
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        rule = digitalocean.ForwardingRule(entry_port=3306,
                                           entry_protocol='tcp',
                                           target_port=3306,
                                           target_protocol='tcp')

        self.lb.remove_forwarding_rules([rule])

        req_body = json.loads("""{
  "forwarding_rules": [
    {
      "entry_protocol": "tcp",
      "entry_port": 3306,
      "target_protocol": "tcp",
      "target_port": 3306,
      "certificate_id": "",
      "tls_passthrough": false
    }
  ]
}""")
        body = json.loads(responses.calls[0].request.body)

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(sorted(body.items()), sorted(req_body.items()))


if __name__ == '__main__':
    unittest.main()
