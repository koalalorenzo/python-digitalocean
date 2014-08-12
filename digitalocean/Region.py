from .baseapi import BaseAPI

class Region(BaseAPI):
    name = None
    slug = None
    sizes = []
    available = None
    features = []

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__()

        #Setting the attribute values
        for attr in kwargs.keys():
            setattr(self,attr,kwargs[attr])
