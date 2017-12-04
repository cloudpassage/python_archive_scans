#!/usr/bin/python
# -*- coding: utf-8 -*-
from api_controller import ApiController


class ScansController(object):
    def __init__(self):
        self.api = ApiController()

    def index(self, **kwargs):
        return self.api.get_paginated("/v1/scans", **kwargs)

    def show(self, scan_id):
        return self.api.get("/v1/scans/%s" % scan_id)
