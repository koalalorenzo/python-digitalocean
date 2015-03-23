# -*- coding: utf-8 -*-
import json
import logging
import requests
try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin


GET = 'GET'
POST = 'POST'
DELETE = 'DELETE'
PUT = 'PUT'


class Error(Exception):
    """Base exception class for this module"""
    pass


class TokenError(Error):
    pass


class DataReadError(Error):
    pass


class JSONReadError(Error):
    pass


class BaseAPI(object):
    """
        Basic api class for
    """
    token = ""
    end_point = "https://api.digitalocean.com/v2/"

    def __init__(self, *args, **kwargs):
        self.token = ""
        self.end_point = "https://api.digitalocean.com/v2/"
        self._log = logging.getLogger(__name__)

        """
          Addition:
            Added api call count variables.

          Description:
            Useful for checking remaining call count before sending api request,
            and keeping track of api calls used.
            
          Warning:
            This is not fully implimented, and does not affect any api calls.
            At the moment the only thing that relies on this is Backup.py.
        """
        self.api_calls_limit      = 5000
        self.api_calls_remaining  = 1
        self.api_calls_used       = 0

        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

    def __perform_request(self, url, type=GET, params=None):
        """
            This method will perform the real request,
            in this way we can customize only the "output" of the API call by
            using self.__call_api method.
            This method will return the request object.
        """
        if params is None: params = {}

        if not self.token:
            raise TokenError("No token provided. Please use a valid token")

        if "https" not in url:
            url = urljoin(self.end_point, url)

        # lookup table to find out the apropriate requests method,
        # headers and payload type (json or query parameters)
        identity = lambda x: x
        json_dumps = lambda x: json.dumps(x)
        lookup = {
            GET: (requests.get, {}, 'params', identity),
            POST: (requests.post, {'Content-type': 'application/json'}, 'data',
                   json_dumps),
            PUT: (requests.put, {'Content-type': 'application/json'}, 'data',
                  json_dumps),
            DELETE: (requests.delete,
                     {'content-type': 'application/x-www-form-urlencoded'},
                     'params', identity),
        }

        requests_method, headers, payload, transform = lookup[type]
        headers.update({'Authorization': 'Bearer ' + self.token})
        kwargs = {'headers': headers, payload: transform(params)}

        # remove token from log
        headers_str = str(headers).replace(self.token.strip(), 'TOKEN')
        self._log.debug('%s %s %s:%s %s' %
                        (type, url, payload, params, headers_str))

        return requests_method(url, **kwargs)

    def get_data(self, url, type=GET, params=None):
        """
            This method is a basic implementation of __call_api that checks
            errors too. In cas of success the method will return True or the
            content of the response to the request.
        """
        if params is None: params = dict()

        req = self.__perform_request(url, type, params)

        if req.status_code == 204:
            return True

        try:
            data = req.json()
        except ValueError as e:
            raise JSONReadError('Read failed from DigitalOcean: %s' % e.message)

        if not req.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise DataReadError(msg)

        """
          Addition:
            Added api call count variables.

          Description:
            Useful for checking remaining call count before sending api request,
            and keeping track of api calls used.
        """
        if "ratelimit-limit" in req.headers:
          self.api_calls_limit = int(req.headers["ratelimit-limit"])

        if "ratelimit-remaining" in req.headers:
          self.api_calls_remaining = int(req.headers["ratelimit-remaining"])
          if self.api_calls_used == 0:
            self.api_calls_used = self.api_calls_used+1
        
        self.api_calls_used = (self.api_calls_limit-self.api_calls_remaining) - self.api_calls_used

        return data

    def __str__(self):
        return "%s" % self.token

    def __unicode__(self):
        return u"%s" % self.__str__()

    """
      Addition:
        This property returns a string of the object properties.
      Description:
        Used for a visual representaion to see the object
        details in the console while testing.
      Example:
        print( droplet.details )
    """
    @property
    def details(self):
      details = ""
      for key in self.__dict__.keys():
        details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
      self._details = details
      return self._details
