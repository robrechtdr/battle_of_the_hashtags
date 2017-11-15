# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    #https://stackoverflow.com/questions/7115097/the-right-place-to-keep-my-signals-py-files-in-django/21612050#21612050
    def ready(self):
        import core.signals
