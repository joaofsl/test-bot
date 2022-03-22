#!/usr/bin/python
# -*- coding: utf-8 -*-

import string

import appier.legacy

import ripe_compose.logic

class Logic(ripe_compose.logic.Logic):

    def supported_characters(self, group, index, ctx):
        return string.ascii_letters + string.digits
