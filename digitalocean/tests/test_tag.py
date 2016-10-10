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

        responses.add(responses.GET,
                      self.base_url + "tags/awesome",
                      body=data,
                      status=200,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.load()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome")
        self.assertEqual(droplet_tag.name,
                         "awesome")


    @responses.activate
    def test_create(self):
        data = self.load_from_file('tags/single.json')

        responses.add(responses.POST,
                      self.base_url + "tags/",
                      body=data,
                      status=201,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/")
        self.assertEqual(droplet_tag.name, "awesome")

    @responses.activate
    def test_update_tag(self):
        data = self.load_from_file('tags/updatetag.json')

        responses.add(responses.PUT,
                      self.base_url + "tags/awesome",
                      body=data,
                      status=200,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.update_tag(name="extra-awesome")

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome")
        self.assertEqual(droplet_tag.name, "extra-awesome")


    @responses.activate
    def test_delete(self):
        responses.add(responses.DELETE,
                      self.base_url + "tags/awesome",
                      status=204,
                      content_type='application/json')

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.delete()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome")
        self.assertEqual(droplet_tag.name, "awesome")


    @responses.activate
    def test_add_droplets(self):
        data = self.load_from_file('tags/resources.json')

        responses.add(responses.POST,
                      self.base_url + "tags/awesome/resources",
                      body=data,
                      status=204,
                      content_type='application/json')

        resource_id = json.loads(data)["resources"][0]["resource_id"]

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.add_droplets([resource_id])

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome/resources")


    @responses.activate
    def test_remove_droplets(self):
        data = self.load_from_file('tags/resources.json')

        responses.add(responses.DELETE,
                      self.base_url + "tags/awesome/resources",
                      body=data,
                      status=201,
                      content_type='application/json')

        resource_id = json.loads(data)["resources"][0]["resource_id"]

        droplet_tag = digitalocean.Tag(name='awesome', token=self.token)
        droplet_tag.remove_droplets([resource_id])

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "tags/awesome/resources")


if __name__ == '__main__':
    unittest.main()
