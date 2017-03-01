import json
import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestCertificate(BaseTest):

    def setUp(self):
        super(TestCertificate, self).setUp()
        self.cert_id = '892071a0-bb95-49bc-8021-3afd67a210bf'
        self.cert = digitalocean.Certificate(id=self.cert_id, token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('certificate/single.json')
        url = self.base_url + 'certificates/' + self.cert_id

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.cert.load()

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(self.cert.id, self.cert_id)
        self.assertEqual(self.cert.name, 'web-cert-01')
        self.assertEqual(self.cert.sha1_fingerprint,
            'dfcc9f57d86bf58e321c2c6c31c7a971be244ac7')
        self.assertEqual(self.cert.not_after, '2017-02-22T00:23:00Z')
        self.assertEqual(self.cert.created_at, '2017-02-08T16:02:37Z')

    @responses.activate
    def test_create_ids(self):
        data = self.load_from_file('certificate/single.json')
        url = self.base_url + 'certificates/'

        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        cert = digitalocean.Certificate(name='web-cert-01',
                                        private_key = "a-b-c",
                                        leaf_certificate = "e-f-g",
                                        certificate_chain = "a-b-c\ne-f-g",
                                        token=self.token).create()

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(cert.id, '892071a0-bb95-49bc-8021-3afd67a210bf')
        self.assertEqual(cert.name, 'web-cert-01')
        self.assertEqual(cert.sha1_fingerprint,
            'dfcc9f57d86bf58e321c2c6c31c7a971be244ac7')
        self.assertEqual(cert.not_after, '2017-02-22T00:23:00Z')
        self.assertEqual(cert.created_at, '2017-02-08T16:02:37Z')

    @responses.activate
    def test_destroy(self):
        url = self.base_url + 'certificates/' + self.cert_id
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        self.cert.destroy()

        self.assertEqual(responses.calls[0].request.url, url)


if __name__ == '__main__':
    unittest.main()
