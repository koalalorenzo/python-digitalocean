import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestImage(BaseTest):

    def setUp(self):
        super(TestImage, self).setUp()
        self.image = digitalocean.Image(
            id=449676856, slug='testslug', token=self.token
        )

    @responses.activate
    def test_load(self):
        data = self.load_from_file('images/single.json')
        url = "{}images/{}".format(self.base_url, self.image.id)

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.image.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.image.id, 449676856)
        self.assertEqual(self.image.slug, 'testslug')
        self.assertEqual(self.image.name, 'My Snapshot')
        self.assertEqual(self.image.distribution, 'Ubuntu')
        self.assertEqual(self.image.public, False)
        self.assertEqual(self.image.created_at, "2014-08-18T16:35:40Z")
        self.assertEqual(self.image.size_gigabytes, 2.34)
        self.assertEqual(self.image.min_disk_size, 20)

    @responses.activate
    def test_load_by_slug(self):
        """Test loading image by slug."""
        data = self.load_from_file('images/single.json')
        url = "{}images/{}".format(self.base_url, self.image.slug)
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.image.load(use_slug=True)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.image.id, 449676856)
        self.assertEqual(self.image.slug, 'testslug')
        self.assertEqual(self.image.name, 'My Snapshot')
        self.assertEqual(self.image.distribution, 'Ubuntu')
        self.assertEqual(self.image.public, False)
        self.assertEqual(self.image.created_at, "2014-08-18T16:35:40Z")
        self.assertEqual(self.image.size_gigabytes, 2.34)
        self.assertEqual(self.image.min_disk_size, 20)

    @responses.activate
    def test_destroy(self):
        responses.add(responses.DELETE,
                      '{}images/{}/'.format(self.base_url, self.image.id),
                      status=204,
                      content_type='application/json')

        self.image.destroy()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + 'images/449676856/')

    @responses.activate
    def test_transfer(self):
        data = self.load_from_file('images/transfer.json')

        responses.add(responses.POST,
                      '{}images/{}/actions/'.format(
                        self.base_url, self.image.id),
                      body=data,
                      status=201,
                      content_type='application/json')

        res = self.image.transfer(new_region_slug='lon1')

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + 'images/449676856/actions/')
        self.assertEqual(res['action']['type'], 'transfer')
        self.assertEqual(res['action']['status'], 'in-progress')
        self.assertEqual(res['action']['id'], 68212728)

    @responses.activate
    def test_rename(self):
        data = self.load_from_file('images/rename.json')

        responses.add(responses.PUT,
                      '{}images/{}'.format(self.base_url, self.image.id),
                      body=data,
                      status=200,
                      content_type='application/json')

        res = self.image.rename(new_name='Descriptive name')

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + 'images/449676856')
        self.assertEqual(res['image']['name'], 'Descriptive name')


if __name__ == '__main__':
    unittest.main()
