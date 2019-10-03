import os
try:
    import mock
except ImportError:
    from unittest import mock

import responses
import requests
import digitalocean

from .BaseTest import BaseTest


class TestBaseAPI(BaseTest):

    def setUp(self):
        super(TestBaseAPI, self).setUp()
        self.manager = digitalocean.Manager(token=self.token)
        self.user_agent = "{0}/{1} {2}/{3}".format('python-digitalocean',
                                                   digitalocean.__version__,
                                                   requests.__name__,
                                                   requests.__version__)

    @responses.activate
    def test_user_agent(self):
        data = self.load_from_file('account/account.json')

        url = self.base_url + 'account/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.manager.get_account()

        self.assertEqual(responses.calls[0].request.headers['User-Agent'],
                         self.user_agent)

    @responses.activate
    def test_customize_session(self):
        data = self.load_from_file('account/account.json')
        url = self.base_url + 'account/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.manager._session.proxies['https'] = 'https://127.0.0.1:3128'
        self.manager.get_account()

    def test_custom_endpoint(self):
        custom_endpoint = 'http://example.com/'

        with mock.patch.dict(os.environ,
                            {'DIGITALOCEAN_END_POINT': custom_endpoint},
                            clear=True):
            base_api = digitalocean.baseapi.BaseAPI()
            
            self.assertEqual(base_api.end_point, custom_endpoint)

    def test_invalid_custom_endpoint(self):
        custom_endpoint = 'not a valid endpoint'

        with mock.patch.dict(os.environ,
                            {'DIGITALOCEAN_END_POINT': custom_endpoint},
                            clear=True):
            self.assertRaises(digitalocean.EndPointError, digitalocean.baseapi.BaseAPI)
