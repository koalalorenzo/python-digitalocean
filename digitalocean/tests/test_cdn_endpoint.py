import json
import unittest

import responses

import digitalocean
from .BaseTest import BaseTest


class TestCDNRecord(BaseTest):

    def setUp(self):
        super(TestCDNRecord, self).setUp()

    @responses.activate
    def test_load(self):
        data = self.load_from_file('cdn_endpoints/single.json')

        url = self.base_url + "cdn/endpoints/19f06b6a-3ace-4315-b086-499a0e521b76"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')
        c = digitalocean.CDNEndpoint(id='19f06b6a-3ace-4315-b086-499a0e521b76', token=self.token).load()
        self.assertEqual(c.id, '19f06b6a-3ace-4315-b086-499a0e521b76')
        self.assertEqual(c.origin, 'static-images.nyc3.digitaloceanspaces.com')
        self.assertEqual(c.endpoint, 'static-images.nyc3.cdn.digitaloceanspaces.com')
        self.assertEqual(c.created_at, '2018-07-19T15:04:16Z')
        self.assertEqual(c.ttl, 3600)

    @responses.activate
    def test_create(self):
        data = self.load_from_file('cdn_endpoints/single.json')

        url = self.base_url + "cdn/endpoints"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        cdn_endpoint = digitalocean.CDNEndpoint(origin='static-images.nyc3.digitaloceanspaces.com', token=self.token)
        cdn_endpoint.create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "cdn/endpoints")
        self.assertEqual(cdn_endpoint.origin, "static-images.nyc3.digitaloceanspaces.com")


    @responses.activate
    def test_delete(self):
        url = self.base_url + "cdn/endpoints/19f06b6a-3ace-4315-b086-499a0e521b76"
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        cdn_endpoint = digitalocean.CDNEndpoint(id='19f06b6a-3ace-4315-b086-499a0e521b76', token=self.token)
        cdn_endpoint.delete()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "cdn/endpoints/19f06b6a-3ace-4315-b086-499a0e521b76")
        self.assertEqual(cdn_endpoint.id, '19f06b6a-3ace-4315-b086-499a0e521b76')

    @responses.activate
    def test_save(self):
        data = self.load_from_file('cdn_endpoints/single.json')
        url = self.base_url + "cdn/endpoints/19f06b6a-3ace-4315-b086-499a0e521b76"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')
        c = digitalocean.CDNEndpoint(id='19f06b6a-3ace-4315-b086-499a0e521b76', token=self.token).load()
        self.assertEqual(c.ttl, 3600)
        c.ttl = 60

        data = self.load_from_file('cdn_endpoints/update.json')
        url = self.base_url + "cdn/endpoints/19f06b6a-3ace-4315-b086-499a0e521b76"
        responses.add(responses.PUT,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')
        c.save()
        self.assertEqual(c.ttl, 60)


if __name__ == '__main__':
    unittest.main()
