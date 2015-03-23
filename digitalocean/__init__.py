# -*- coding: utf-8 -*-
"""digitalocean API to manage droplets"""

__version__ = "1.4.2"
__author__ = "Lorenzo Setale ( http://who.is.lorenzo.setale.me/? )"
__author_email__ = "koalalorenzo@gmail.com"
__license__ = "See: http://creativecommons.org/licenses/by-nd/3.0/ "
__copyright__ = "Copyright (c) 2012, 2013, 2014 Lorenzo Setale"

from .Manager import Manager
from .Droplet import Droplet, DropletError, BadKernelObject, BadSSHKeyFormat
from .Region import Region
from .Size import Size
from .Image import Image
from .Action import Action
from .Backup import Backup
from .Account import Account
from .Domain import Domain
from .Record import Record
from .SSHKey import SSHKey
from .Kernel import Kernel
from .baseapi import Error, TokenError, DataReadError
