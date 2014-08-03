class Region(object):
    def __init__(self, token=""):
        self.token = token
        self.name = None
        self.slug = None
        self.sizes = []
        self.available = None
        self.features = []