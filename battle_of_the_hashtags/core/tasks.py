# Create your tasks here
from __future__ import absolute_import, unicode_literals

import datetime
import re

import tweepy

from enchant.checker import SpellChecker

from django.utils import timezone

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .models import HashtagBattle, ProcessedTweet



def batch_process_hashtag_battle(battle, batch_size=10):
    """
    Cautiously batch processing instead of continuously processing as to avoid getting blocked as twitter's api is rate limited.

    https://stackoverflow.com/questions/21305547/how-rate-limit-works-in-twitter-in-search-api

    In a more advanced version we should count the 'already processed entries'-checking as well in the batch size.
    The more popular the hashtags involved (getting lots of entries per second on average) the less important this is,
    for simplity now assuming we use very popular hashtags. 
    """
    # Should be read from env vars/separate file:
    consumer_key = "SzIBHiCh8OgQ8YNCv0QQzKIIy"
    consumer_secret = "uN4YWWiIit98K07loiei0SVTkU5GKesqC6qxeVHkTBiopPscao"
    access_token = "930514548427251712-aVMXgmmzpSQfjuEZ39xhmIw1CokVKfH"
    access_token_secret = "ocFqV72Hl80Cx7r0aVl3LgJQH08QJgihLR9Zmg9q1TwGj"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Twitter api by default only shows tweets not older than a week.
    # https://stackoverflow.com/questions/24214189/how-can-i-get-tweets-older-than-a-week-using-tweepy-or-other-python-libraries
    api = tweepy.API(auth)

    # Ideally we connect with a service that constantly updates with new spelling like
    # Grammerly
    # For now:
    # http://pythonhosted.org/pyenchant/tutorial.html
    #us_sc = Spellchecker("en_US")
    gb_spchecker = SpellChecker("en_GB")

    htag_1_curs = tweepy.Cursor(api.search, q="#{}".format(battle.hashtag_1))
    htag_2_curs = tweepy.Cursor(api.search, q="#{}".format(battle.hashtag_2))

    htag_1_gen = htag_1_curs.items()
    htag_2_gen = htag_2_curs.items()
    
    # Why a while loop with calling the generator explicitly with next() ?
    # Initially wanted to try:
    # 'for htag_1_tweet, htag_2_tweet in zip(htag_1_curs.items(), htag_2_curs.items()):'
    # However; ideally we don't want to skip processing of a tweet of one htag just because the tweet of 
    # the other htag already happens to be processed. 
    ct = 0
    both_hashtagslists_still_have_unprocessed_tweets = True
    while both_hashtagslists_still_have_unprocessed_tweets:
        print ct

        if ct == batch_size:
            # We don't want to hit the rate limit.
            break

        def get_next_tweet_to_process(htag_gen):
            htag_tweet = next(htag_gen)
            processed_tweet = ProcessedTweet.objects.filter(tweet_id=htag_tweet.id).first()
            if processed_tweet:
                print "Skip already processed tweet {}".format(processed_tweet.tweet_id)
                htag_gen, htag_tweet = get_next_tweet_to_process(htag_gen)
            return htag_gen, htag_tweet

        try:
            print "getting htag 1 next tweet"
            htag_1_gen, htag_1_tweet = get_next_tweet_to_process(htag_1_gen)
        except StopIteration:
            # The same as doing a break but nicer as it is based on while condition
            both_hashtagslists_still_have_unprocessed_tweets = False
            continue
        try:
            print "getting htag 2 next tweet"
            htag_2_gen, htag_2_tweet = get_next_tweet_to_process(htag_2_gen)
        except StopIteration:
            both_hashtagslists_still_have_unprocessed_tweets = False
            continue
        

        # This can of course be hugely extended but just a bare bones version
        # to demo pattern.
        def filter_out_words_to_ignore_in_spell_check(text):
            """
            We don't want to apply spell checking to all words
            """
            # Get rid of urls
            # https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
            text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
            return text

        cleaned_htag_1_tweet_text = filter_out_words_to_ignore_in_spell_check(htag_1_tweet.text)
        gb_spchecker.set_text(cleaned_htag_1_tweet_text)
        htag_1_errors = [err.word for err in gb_spchecker]
        battle.hashtag_1_cur_typos += len(htag_1_errors)

        cleaned_htag_2_tweet_text = filter_out_words_to_ignore_in_spell_check(htag_2_tweet.text)
        gb_spchecker.set_text(cleaned_htag_2_tweet_text)
        htag_2_errors = [err.word for err in gb_spchecker]
        battle.hashtag_2_cur_typos += len(htag_2_errors)
        
        print "htag 1 errors: {}".format(battle.hashtag_1_cur_typos)
        print "htag 2 errors: {}".format(battle.hashtag_2_cur_typos)

        if battle.hashtag_1_cur_typos < battle.hashtag_2_cur_typos:
            battle.cur_winner = battle.hashtag_1
        elif battle.hashtag_1_cur_typos > battle.hashtag_2_cur_typos:
            battle.cur_winner = battle.hashtag_2
        else:
            # Semantically None would be more correct but person checking is going to
            # be less sure that it is a draw.
            battle_cur_winner = "draw"

        battle.save()

        processed_htag_1_tweet = ProcessedTweet(tweet_id=htag_1_tweet.id)
        processed_htag_1_tweet.save()
        processed_htag_2_tweet = ProcessedTweet(tweet_id=htag_2_tweet.id)
        processed_htag_2_tweet.save()

        ct += 1

    print "current winner: {}".format(battle.cur_winner)


@periodic_task(run_every=(crontab(minute='*')), name="engage_battles", ignore_result=True)
def engage_battle():   
    for battle in HashtagBattle.objects.all():
        now = timezone.now()
        # To be safe we stop calculation a bit early as otherwise would seem like time passed but it still needs to finish calculating.
        if battle.start_date <= now and now < battle.end_date - datetime.timedelta(seconds=30):
            batch_process_hashtag_battle(battle) 
