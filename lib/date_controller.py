#!/usr/bin/python
# -*- coding: utf-8 -*-
from dateutil.parser import parse


class DateController(object):
    def iso8601(self, date):
        return parse(date).strftime("%Y-%m-%d")
