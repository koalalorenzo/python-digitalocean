# -*- coding: utf-8 -*-
import requests
from urlparse import urljoin

class BaseAPI(object):
    """
        Basic api class for
    """
    token = ""
    call_response = None
    end_point = "https://api.digitalocean.com/v2/"

    def __init__(self, *args, **kwargs):
        self.token = ""
        self.call_response = None
        self.end_point = "https://api.digitalocean.com/v2/"

        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])

    def __perform_get(self, url, headers=dict(), params=dict()):
        return requests.get(url, headers=headers, params=params)

    def __perform_post(self, url, headers=dict(), params=dict()):
        headers['content-type'] = 'application/json'
        return requests.post(url, headers=headers, params=params)

    def __perform_put(self, url, headers=dict(), params=dict()):
        headers['content-type'] = 'application/json'
        return requests.put(url, headers=headers, params=params)

    def __perform_delete(self, url, headers=dict(), params=dict()):
        headers['content-type'] = 'application/x-www-form-urlencoded'
        return requests.delete(url, headers=headers, params=params)

    def __perform_request(self, url, type='GET', params=dict(), headers=dict()):
        """
            This method will perform the real request,
            in this way we can customize only the "output" of the API call by
            using self.__call_api method.
            This method will return the request object.
        """
        if not self.token:
            raise Exception("No token provied. Please use a valid token")

        if "https" not in url:
            url = urljoin(self.end_point, url)

        headers.update({'Authorization':'Bearer ' + self.token})
        if type == 'POST':
            r = self.__perform_post(url, headers=headers, params=params)
        elif type == 'PUT':
            r = self.__perform_put(url, headers=headers, params=params)
        elif type == 'DELETE':
            r = self.__perform_delete(url, headers=headers, params=params)
        else:
            r = self.__perform_get(url, headers=headers, params=params)
        return r

    def get_data(self, url, type="GET", params=dict()):
        """
            This method is a basic implementation of __call_api that checks
            errors too. In cas of success the method will return True or the
            content of the response to the request.
        """
        req = self.__perform_request(url, type, params)
        if req.status_code == 204:
            return True

        data = req.json()
        if not req.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise Exception(msg)
        return data

    def __str__(self):
        return "%s" % self.token

    def __unicode__(self):
        return u"%s" % self.__str__()
