import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestVolume(BaseTest):

    def setUp(self):
        super(TestVolume, self).setUp()
        self.volume = digitalocean.Volume(
            id='506f78a4-e098-11e5-ad9f-000f53306ae1', token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('volumes/single.json')
        volume_path = "volumes/506f78a4-e098-11e5-ad9f-000f53306ae1"

        responses.add(responses.GET,
                      self.base_url + volume_path,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.volume.load()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + volume_path)
        self.assertEqual(self.volume.id,
                         "506f78a4-e098-11e5-ad9f-000f53306ae1")
        self.assertEqual(self.volume.size_gigabytes, 100)

    @responses.activate
    def test_create(self):
        data = self.load_from_file('volumes/single.json')

        responses.add(responses.POST,
                      self.base_url + "volumes/",
                      body=data,
                      status=201,
                      content_type='application/json')

        volume = digitalocean.Volume(droplet_id=12345,
                                     region='nyc1',
                                     size_gigabytes=100,
                                     token=self.token).create()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "volumes/")
        self.assertEqual(volume.id, "506f78a4-e098-11e5-ad9f-000f53306ae1")
        self.assertEqual(volume.size_gigabytes, 100)

    @responses.activate
    def test_destroy(self):
        volume_path = "volumes/506f78a4-e098-11e5-ad9f-000f53306ae1/"
        responses.add(responses.DELETE,
                      self.base_url + volume_path,
                      status=204,
                      content_type='application/json')

        self.volume.destroy()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + volume_path)

    @responses.activate
    def test_attach(self):
        data = self.load_from_file('volumes/attach.json')
        volume_path = "volumes/" + self.volume.id + "/actions/"

        responses.add(responses.POST, self.base_url + volume_path,
                      body=data,
                      status=201,
                      content_type='application/json')

        res = self.volume.attach(droplet_id=12345, region='nyc1')

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + volume_path)
        self.assertEqual(res['action']['type'], 'attach_volume')
        self.assertEqual(res['action']['status'], 'completed')
        self.assertEqual(res['action']['id'], 72531856)

    @responses.activate
    def test_detach(self):
        data = self.load_from_file('volumes/detach.json')
        volume_path = "volumes/" + self.volume.id + "/actions/"

        responses.add(responses.POST, self.base_url + volume_path,
                      body=data,
                      status=201,
                      content_type='application/json')

        res = self.volume.detach(droplet_id=12345, region='nyc1')

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + volume_path)
        self.assertEqual(res['action']['type'], 'detach_volume')
        self.assertEqual(res['action']['status'], 'in-progress')
        self.assertEqual(res['action']['id'], 68212773)

    @responses.activate
    def test_resize(self):
        data = self.load_from_file('volumes/resize.json')
        volume_path = "volumes/" + self.volume.id + "/actions/"

        responses.add(responses.POST, self.base_url + volume_path,
                      body=data,
                      status=201,
                      content_type='application/json')

        res = self.volume.resize(region='nyc1',
                                 size_gigabytes=1000)

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + volume_path)
        self.assertEqual(res['action']['type'], 'resize_volume')
        self.assertEqual(res['action']['status'], 'in-progress')
        self.assertEqual(res['action']['id'], 72531856)

if __name__ == '__main__':
    unittest.main()
