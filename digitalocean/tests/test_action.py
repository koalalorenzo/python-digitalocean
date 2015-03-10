import unittest
import responses
import json
import digitalocean

from .BaseTest import BaseTest


class TestAction(BaseTest):

    def setUp(self):
        super(TestAction, self).setUp()
        self.action = digitalocean.Action(id=39388122, token=self.token)

    @responses.activate
    def test_load_directly(self):
        data = self.load_from_file('actions/ipv6_completed.json')

        responses.add(responses.GET, self.base_url + "actions/39388122",
                      body=data,
                      status=200,
                      content_type='application/json')

        self.action.load_directly()

        self.assertEqual(responses.calls[0].request.url,
                         self.base_url + "actions/39388122")
        self.assertEqual(self.action.status, "completed")
        self.assertEqual(self.action.id, 39388122)
        self.assertEqual(self.action.region_slug, 'nyc3')

if __name__ == '__main__':
    unittest.main()
