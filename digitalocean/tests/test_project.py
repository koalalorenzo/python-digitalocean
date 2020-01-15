import json
import unittest

import responses

import digitalocean
from .BaseTest import BaseTest


class TestProject(BaseTest):

    def setUp(self):
        super(TestProject, self).setUp()
        self.project = digitalocean.Project(
            id='4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679', token=self.token , owner_id='99525febec065ca37b2ffe4f852fd2b2581895e7')

    @responses.activate
    def test_load(self):
        data = self.load_from_file('volumes/single.json')
        volume_path = "volumes/506f78a4-e098-11e5-ad9f-000f53306ae1"

        url = self.base_url + volume_path
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.volume.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.volume.id,
                         "506f78a4-e098-11e5-ad9f-000f53306ae1")
        self.assertEqual(self.volume.size_gigabytes, 100)