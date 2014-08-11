import requests
from urlparse import urljoin

class BaseAPI(object):
    """
        Basic api class for
    """
    token = ""
    call_response = None
    end_point = "https://api.digitalocean.com/v2/"

    def __init__(self):
        super(BaseAPI, self).__init__()
        self.token = ""
        self.call_response = None
        self.end_point = "https://api.digitalocean.com/v2/"

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

    def __perform_request(self, url, type='GET', params=dict()):
        """
            This method will perform the real request,
            in this way we can customize only the "output" of the API call by
            using self.__call_api method.
            This method will return the request object.
        """
        if not self.token:
            raise Exception("No token provied. Please use a valid token")

        if not "https" not in url:
            url = urljoin(self.end_point, url)

        headers = {'Authorization':'Bearer ' + self.token}
        if type == 'POST':
            r = self.__perform_request(url, headers=headers, params=params)
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
            errors too.
        """
        req = self.__perform_request(url, type, params)
        data = req.json()
        if req.status_code != requests.codes.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise Exception(msg)
        return data
