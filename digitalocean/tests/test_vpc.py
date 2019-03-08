import json
import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestVPC(BaseTest):

    def setUp(self):
        super(TestVPC, self).setUp()
        self.vpc_id = '5a4981aa-9653-4bd1-bef5-d6bff52042e4'
        self.vpc = digitalocean.VPC(id=self.vpc_id, token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('vpcs/single.json')
        url = self.base_url + 'vpcs/' + self.vpc_id

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.vpc.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.vpc.id, self.vpc_id)
        self.assertEqual(self.vpc.name, 'my-new-vpc')
        self.assertEqual(self.vpc.region, 'nyc1')
        self.assertEqual(self.vpc.ip_range, '10.10.10.0/24')
        self.assertEqual(self.vpc.description, '')
        self.assertEqual(self.vpc.urn,
          'do:vpc:5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(self.vpc.created_at, '2020-03-13T18:48:45Z')
        self.assertEqual(self.vpc.default, False)

    @responses.activate
    def test_create(self):
        data = self.load_from_file('vpcs/single.json')
        url = self.base_url + 'vpcs'

        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        vpc = digitalocean.VPC(name='my-new-vpc',
                               region='nyc1',
                               ip_range='10.10.10.0/24',
                               token=self.token).create()

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(vpc.id, '5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(vpc.name, 'my-new-vpc')
        self.assertEqual(vpc.ip_range, '10.10.10.0/24')
        self.assertEqual(vpc.description, '')
        self.assertEqual(vpc.urn, 'do:vpc:5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(vpc.created_at, '2020-03-13T18:48:45Z')

    @responses.activate
    def test_rename(self):
        data = self.load_from_file('vpcs/single.json')
        url = self.base_url + 'vpcs/' + self.vpc_id
        responses.add(responses.PATCH,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.vpc.rename('my-new-vpc')

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(self.vpc.id, '5a4981aa-9653-4bd1-bef5-d6bff52042e4')
        self.assertEqual(self.vpc.name, 'my-new-vpc')
        self.assertEqual(self.vpc.created_at, '2020-03-13T18:48:45Z')

    @responses.activate
    def test_destroy(self):
        url = self.base_url + 'vpcs/' + self.vpc_id
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        self.vpc.destroy()

        self.assertEqual(responses.calls[0].request.url, url)


if __name__ == '__main__':
    unittest.main()
