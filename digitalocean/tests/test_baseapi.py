import os

from digitalocean.baseapi import BaseAPI
try:
    import mock
except ImportError:
    from unittest import mock

import random
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

    def test_get_data_error_response_no_body(self):
        with mock.patch.object(self.manager, '_BaseAPI__perform_request') as mock_4xx_response:
            mock_4xx_response.return_value = requests.Response()
            mock_4xx_response.return_value._content = b''
            mock_4xx_response.return_value.status_code = random.randint(400, 499) # random 4xx status code

            self.assertRaises(requests.HTTPError, self.manager.get_data, 'test')
        
        with mock.patch.object(self.manager, '_BaseAPI__perform_request') as mock_5xx_response:
            mock_5xx_response.return_value = requests.Response()
            mock_5xx_response.return_value._content = b'' 
            mock_5xx_response.return_value.status_code = random.randint(500, 599) # random 5xx status code

            self.assertRaises(requests.HTTPError, self.manager.get_data, 'test')
