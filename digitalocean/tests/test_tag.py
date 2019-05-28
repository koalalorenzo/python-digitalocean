import unittest
import responses
import digitalocean
import json

from .BaseTest import BaseTest


class TestTags(BaseTest):

    def setUp(self):
        super(TestTags, self).setUp()

    @responses.activate
    def test_load(self):
        data = self.load_from_file('tags/single.json')

        url = self.base_url + "tags/awesome"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(droplet_tag.name,
                         "awesome")


    @responses.activate
    def test_create(self):
        data = self.load_from_file('tags/single.json')

        url = self.base_url + "tags"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags")
        self.assertEqual(droplet_tag.name, "awesome")


    @responses.activate
    def test_delete(self):
        url = self.base_url + "tags/awesome"
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.delete()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome")
        self.assertEqual(droplet_tag.name, "awesome")


    @responses.activate
    def test_add_droplets(self):
        url = self.base_url + "tags/awesome/resources"
        responses.add(responses.POST,
                      url,
                      status=204,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.add_droplets(["9569411"])

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome/resources")


    @responses.activate
    def test_remove_droplets(self):
        url = self.base_url + "tags/awesome/resources"
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.remove_droplets(["9569411"])

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome/resources")


    @responses.activate
    def test_add_volume_snapshots(self):
        url = self.base_url + "tags/awesome/resources"
        responses.add(responses.POST,
                      url,
                      status=204,
                      content_type='application/json')

        tag = digitalocean.Tag(name='awesome', token=self.token)
        tag.add_snapshots(["9569411"])

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome/resources")


    @responses.activate
    def test_remove_volume_snapshots(self):
        url = self.base_url + "tags/awesome/resources"
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        tag = digitalocean.Tag(name='awesome', token=self.token)
        tag.remove_snapshots(["9569411"])

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome/resources")


if __name__ == '__main__':
    unittest.main()
