#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config(object):

    def on_install(self, ctx):
        print("Thank you for installing the cariuma package")
        print("For more information send an email to development@platforme.com")

    def on_uninstall(self):
        print("We're sorry to see you leave cariuma")
