from .baseapi import BaseAPI

class Size(BaseAPI):
    slug = None
    memory = None
    vcpus = None
    disk = None
    transfer = None
    price_monthly = None
    price_hourly = None
    regions = []

    def __init__(self, token=""):
        super(Size, self).__init__()
        if token:
            self.token = token
