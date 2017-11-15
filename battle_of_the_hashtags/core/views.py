# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import HashtagBattle


def home(request):
    return HttpResponse("Welcome home!")


def get_battle(request, pk):
    battle = HashtagBattle.objects.get(pk=pk)
    data = serializers.serialize('json', [battle])
    return HttpResponse(data, content_type='application/json')
