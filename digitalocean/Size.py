class Size(object):
    def __init__(self, token=""):
        self.token = token
        self.slug = None
        self.memory = None
        self.vcpus = None
        self.disk = None
        self.transfer = None
        self.price_monthly = None
        self.price_hourly = None
        self.regions = []