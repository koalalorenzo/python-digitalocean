import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestImage(BaseTest):

    def setUp(self):
        super(TestImage, self).setUp()
        self.image = digitalocean.Image(
            id=449676856,  token=self.token
        )
        self.image_with_slug = digitalocean.Image(
            slug='testslug', token=self.token
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
        self.assertEqual(self.image.name, 'My Snapshot')
        self.assertEqual(self.image.distribution, 'Ubuntu')
        self.assertEqual(self.image.public, False)
        self.assertEqual(self.image.created_at, "2014-08-18T16:35:40Z")
        self.assertEqual(self.image.size_gigabytes, 2.34)
        self.assertEqual(self.image.min_disk_size, 20)

    @responses.activate
    def test_load_by_slug(self):
        """Test loading image by slug."""
        data = self.load_from_file('images/slug.json')
        url = "{}images/{}".format(self.base_url, self.image_with_slug.slug)
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.image_with_slug.load(use_slug=True)

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.image_with_slug.id, None)
        self.assertEqual(self.image_with_slug.slug, 'testslug')
        self.assertEqual(self.image_with_slug.name, 'My Slug Snapshot')
        self.assertEqual(self.image_with_slug.distribution, 'Ubuntu')
        self.assertEqual(self.image_with_slug.public, False)
        self.assertEqual(
            self.image_with_slug.created_at,
            "2014-08-18T16:35:40Z"
        )
        self.assertEqual(self.image_with_slug.size_gigabytes, 2.34)
        self.assertEqual(self.image_with_slug.min_disk_size, 30)

    @responses.activate
    def test_create(self):
        data = self.load_from_file('images/create.json')
        url = self.base_url + "images"

        responses.add(responses.POST,
                      url,
                      body=data,
                      status=202,
                      content_type='application/json')

        image = digitalocean.Image(name='ubuntu-18.04-minimal',
                                   url='https://www.example.com/cloud.img',
                                   distribution='Ubuntu',
                                   region='nyc3',
                                   description='Cloud-optimized image',
                                   tags=['base-image', 'prod'],
                                   token=self.token)
        image.create()

        self.assertEqual(image.id, 38413969)
        self.assertEqual(image.name, 'ubuntu-18.04-minimal')
        self.assertEqual(image.distribution, 'Ubuntu')
        self.assertEqual(image.type, 'custom')
        self.assertEqual(image.status, 'NEW')
        self.assertEqual(image.description, 'Cloud-optimized image')
        self.assertEqual(image.tags, ['base-image', 'prod'])
        self.assertEqual(image.created_at, '2018-09-20T19:28:00Z')

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

    def test_is_string(self):
        self.assertEqual(self.image._is_string("String"), True)
        self.assertEqual(self.image._is_string("1234"), True)
        self.assertEqual(self.image._is_string(123), False)
        self.assertEqual(self.image._is_string(None), None)
        self.assertEqual(self.image._is_string(True), None)
        self.assertEqual(self.image._is_string(False), None)

if __name__ == '__main__':
    unittest.main()
