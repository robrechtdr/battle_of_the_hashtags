# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello!")


def get_battle(request, pk):
    from django.http import JsonResponse
    from .models import HashtagBattle

    from django.core import serializers

    battle = HashtagBattle.objects.get(pk=pk)

    data = serializers.serialize('json', [battle])
    return HttpResponse(data, content_type='application/json')
