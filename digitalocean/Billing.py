# -*- coding: utf-8 -*-
from .baseapi import BaseAPI


class Billing(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.description = None
        self.amount = None
        self.invoice_id = None
        self.invoice_uuid = None
        self.date = None
        self.type = None
        super(Billing, self).__init__(*args, **kwargs)

    def __str__(self):
        return "<Billing: %s>" % (self.invoice_uuid)