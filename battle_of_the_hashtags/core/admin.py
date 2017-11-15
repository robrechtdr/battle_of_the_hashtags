# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import HashtagBattle


@admin.register(HashtagBattle)
class HashtagBattleAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "hashtag_1_cur_typos", "hashtag_2_cur_typos", "cur_winner",)

