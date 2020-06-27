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
        data = self.load_from_file('certificate/custom.json')
        url = self.base_url + 'certificates/' + self.cert_id

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.cert.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.cert.id, self.cert_id)
        self.assertEqual(self.cert.name, 'web-cert-01')
        self.assertEqual(self.cert.sha1_fingerprint,
            'dfcc9f57d86bf58e321c2c6c31c7a971be244ac7')
        self.assertEqual(self.cert.not_after, '2017-02-22T00:23:00Z')
        self.assertEqual(self.cert.created_at, '2017-02-08T16:02:37Z')

    @responses.activate
    def test_create_custom(self):
        data = self.load_from_file('certificate/custom.json')
        url = self.base_url + 'certificates/'

        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        cert = digitalocean.Certificate(name='web-cert-01',
                                        private_key="a-b-c",
                                        leaf_certificate="e-f-g",
                                        certificate_chain="a-b-c\ne-f-g",
                                        type="custom",
                                        token=self.token).create()

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(cert.id, '892071a0-bb95-49bc-8021-3afd67a210bf')
        self.assertEqual(cert.name, 'web-cert-01')
        self.assertEqual(cert.sha1_fingerprint,
            'dfcc9f57d86bf58e321c2c6c31c7a971be244ac7')
        self.assertEqual(cert.not_after, '2017-02-22T00:23:00Z')
        self.assertEqual(cert.created_at, '2017-02-08T16:02:37Z')
        self.assertEqual(cert.type, 'custom')

    @responses.activate
    def test_create_lets_encrypt(self):
        data = self.load_from_file('certificate/lets_encrpyt.json')
        url = self.base_url + 'certificates/'

        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        cert = digitalocean.Certificate(name='web-cert-02',
                                        dns_names=["www.example.com",
                                                   "example.com"],
                                        type="lets_encrpyt",
                                        token=self.token).create()

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(cert.id, 'ba9b9c18-6c59-46c2-99df-70da170a42ba')
        self.assertEqual(cert.name, 'web-cert-02')
        self.assertEqual(cert.sha1_fingerprint,
            '479c82b5c63cb6d3e6fac4624d58a33b267e166c')
        self.assertEqual(cert.not_after, '2018-06-07T17:44:12Z')
        self.assertEqual(cert.created_at, '2018-03-09T18:44:11Z')
        self.assertEqual(cert.type, 'lets_encrypt')
        self.assertEqual(cert.state, 'pending')

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
