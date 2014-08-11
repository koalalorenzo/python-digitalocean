from .baseapi import BaseAPI

class Region(BaseAPI):
    name = None
    slug = None
    sizes = []
    available = None
    features = []

    def __init__(self, token=""):
        super(Region, self).__init__()
        if token:
            self.token = token
