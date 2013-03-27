
"""digitalocean API to manage droplets"""

__version__ = "0.2.2"
__author__ = "Lorenzo Setale ( http://who.is.koalalorenzo.com/? )"
__author_email__ = "koalalorenzo@gmail.com"
__license__ = "See: http://creativecommons.org/licenses/by-nd/3.0/ "
__copyright__ = "Copyright (c) 2012, 2013, 2014 Lorenzo Setale"

from digitalocean.Manager import Manager
from digitalocean.Droplet import Droplet
from digitalocean.Region import Region
from digitalocean.Size import Size
from digitalocean.Image import Image
from digitalocean.Event import Event
