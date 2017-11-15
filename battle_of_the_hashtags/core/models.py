# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# This will have a lot of entries
class ProcessedTweet(models.Model):
    tweet_id = models.IntegerField()


class HashtagBattle(models.Model):
    name = models.CharField(max_length=100) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    hashtag_1 = models.CharField(max_length=100)
    hashtag_1_cur_typos = models.IntegerField(default=0)
    hashtag_2 = models.CharField(max_length=100) 
    hashtag_2_cur_typos = models.IntegerField(default=0)
    cur_winner = models.CharField(max_length=200, blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


'''
hashtag_1 = models.ForeignKey(HashTag)
hashtag_2 = models.ForeignKey(HashTag)

class Hashtag(models.Model):
    name = models.CharField(max_length=100) 
    url = models.URLField(max_length=200)
'''
