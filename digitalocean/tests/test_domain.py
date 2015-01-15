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

    def assert_url_query_equal(self, url1, url2):
        """ Test if two URL queries are equal

        The key=value pairs after the ? in a URL can occur in any order
        (especially since dicts in python 3 are not deterministic across runs).
        The method sorts the key=value pairs and then compares the URLs.
        """
        base1, query1 = url1.split('?')
        base2, query2 = url2.split('?')
        qlist1 = query1.split('&')
        qlist2 = query2.split('&')
        qlist1.sort()
        qlist2.sort()
        new_url1 = base1 + '?' + '&'.join(qlist1)
        new_url2 = base2 + '?' + '&'.join(qlist2)
        self.assertEqual(new_url1, new_url2)

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

        self.assert_url_query_equal(responses.calls[0].request.url,
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

        self.assert_url_query_equal(responses.calls[0].request.url,
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
