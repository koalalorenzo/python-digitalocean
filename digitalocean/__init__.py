# -*- coding: utf-8 -*-
"""digitalocean API to manage droplets"""

__version__ = "1.8"
__author__ = "Lorenzo Setale ( http://who.is.lorenzo.setale.me/? )"
__author_email__ = "koalalorenzo@gmail.com"
__license__ = "LGPL v3"
__copyright__ = "Copyright (c) 2012, 2013, 2014 Lorenzo Setale"

MOCKED = False

from .Manager import Manager
from .Droplet import Droplet, DropletError, BadKernelObject, BadSSHKeyFormat
from .Region import Region
from .Size import Size
from .Image import Image
from .Action import Action
from .Account import Account
from .Domain import Domain
from .Record import Record
from .SSHKey import SSHKey
from .Kernel import Kernel
from .FloatingIP import FloatingIP
from .baseapi import Error, TokenError, DataReadError
