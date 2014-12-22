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
        self.token = "afaketokenthatwillworksincewemockthings"
        self.domain = digitalocean.Domain(name='example.com',
                                          token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('domains/single.json')

        responses.add(responses.GET, self.base_url + "domains/example.com",
                      body=data,
                      status=200,
                      content_type='application/json')

        domain = digitalocean.Domain(name='example.com', token=self.token)
        domain.load()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "domains/example.com")
        self.assertEqual(domain.name, "example.com")
        self.assertEqual(domain.ttl, 1800)

    @responses.activate
    def test_destroy(self):
        responses.add(responses.DELETE, self.base_url + "domains/example.com",
                      status=204,
                      content_type='application/json')

        response = self.domain.destroy()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "domains/example.com")

    @responses.activate
    def test_create_new_domain_record(self):
        data = self.load_from_file('domains/create_record.json')

        responses.add(responses.POST,
                      self.base_url + "domains/example.com/records",
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.domain.create_new_domain_record(type = "CNAME",
                                                        name = "www",
                                                        data = "@")

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + \
                         "domains/example.com/records?type=CNAME&data=%40&name=www")
        self.assertEqual(response['domain_record']['type'], "CNAME")
        self.assertEqual(response['domain_record']['name'], "www")
        self.assertEqual(response['domain_record']['data'], "@")

    @responses.activate
    def test_create(self):
        data = self.load_from_file('domains/create.json')

        responses.add(responses.POST,
                      self.base_url + "domains",
                      body=data,
                      status=201,
                      content_type='application/json')

        domain = digitalocean.Domain(name="example.com",
                                     ip_address="1.1.1.1",
                                     token=self.token).create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + \
                         "domains?ip_address=1.1.1.1&name=example.com")
        self.assertEqual(domain['domain']['name'], "example.com")
        self.assertEqual(domain['domain']['ttl'], 1800)

    @responses.activate
    def test_get_records(self):
        data = self.load_from_file('domains/records.json')

        responses.add(responses.GET,
                      self.base_url + "domains/example.com/records/",
                      body=data,
                      status=200,
                      content_type='application/json')

        records = self.domain.get_records()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "domains/example.com/records/")
        self.assertEqual(len(records), 5)
        self.assertEqual(records[0].type, "A")
        self.assertEqual(records[0].name, "@")
        self.assertEqual(records[4].type, "CNAME")
        self.assertEqual(records[4].name, "example")