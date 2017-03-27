import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestSnapshot(BaseTest):

    def setUp(self):
        super(TestSnapshot, self).setUp()
        self.snapshot = digitalocean.Snapshot(id="fbe805e8-866b-11e6-96bf-000f53315a41", token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('snapshots/single.json')
        url = "{}snapshots/{}".format(self.base_url, self.snapshot.id)

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.snapshot.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.snapshot.id, "fbe805e8-866b-11e6-96bf-000f53315a41")
        self.assertEqual(self.snapshot.name, 'big-data-snapshot1475170902')
        self.assertEqual(self.snapshot.created_at, "2016-09-29T17:41:42Z")
        self.assertEqual(self.snapshot.size_gigabytes, 1.42)
        self.assertEqual(self.snapshot.min_disk_size, 20)

    @responses.activate
    def test_destroy(self):
        responses.add(responses.DELETE,
                      '{}snapshots/{}/'.format(self.base_url, self.snapshot.id),
                      status=204,
                      content_type='application/json')

        self.snapshot.destroy()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + 'snapshots/fbe805e8-866b-11e6-96bf-000f53315a41/')

if __name__ == '__main__':
    unittest.main()
