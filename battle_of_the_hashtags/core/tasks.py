# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.task.schedules import crontab
from celery.decorators import periodic_task

import datetime

@periodic_task(run_every=(crontab(minute='*')), name="engage_battles", ignore_result=True)
def engage_battle():   
    from core.models import HashtagBattle
    from core.signals import batch_process_hashtag_battle

    for battle in HashtagBattle.objects.all():
        from django.utils import timezone
        now = timezone.now()
        #now = datetime.datetime.now()
        # To be safe we stop calculation a bit early as otherwise would seem like time passed but it still needs to finish calculating.
        if battle.start_date <= now and now < battle.end_date - datetime.timedelta(seconds=30):
            batch_process_hashtag_battle(battle) 

