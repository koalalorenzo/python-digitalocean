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

    def __init__(self, *args, **kwargs):
        super(Size, self).__init__()

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])
