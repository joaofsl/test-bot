#!/usr/bin/python
# -*- coding: utf-8 -*-

import base

class Logic(base.Logic):

    def groups(self, ctx):
        return ["main"]

    def minimum_initials(self, group, ctx):
        return 1

    def maximum_initials(self, group, ctx):
        return 8

    def supported_characters(self, group, index, ctx):
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!*? "
