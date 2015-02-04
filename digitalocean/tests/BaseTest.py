import os
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api.digitalocean.com/v2/"
        self.token = "afaketokenthatwillworksincewemockthings"

    def load_from_file(self, json_file):
        cwd = os.path.dirname(__file__)
        with open(os.path.join(cwd, 'data/%s' % json_file), 'r') as f:
            return f.read()

    def split_url(self, url):
        bits = url.split('?')
        if len(bits) == 1:
            return url, []

        qlist = bits[1].split('&')
        qlist.sort()
        return bits[0], qlist

    def assert_url_query_equal(self, url1, url2):
        """ Test if two URL queries are equal

        The key=value pairs after the ? in a URL can occur in any order
        (especially since dicts in python 3 are not deterministic across runs).
        The method sorts the key=value pairs and then compares the URLs.
        """

        base1, qlist1 = self.split_url(url1)
        base2, qlist2 = self.split_url(url2)

        self.assertEqual(base1, base2)
        self.assertEqual(qlist1, qlist2)
