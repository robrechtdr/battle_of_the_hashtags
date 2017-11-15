import datetime
import factory

from .models import HashtagBattle


class HashtagBattleFactoryOne(factory.DjangoModelFactory):
    name = "Hashtag Battle One"
    start_date = datetime.datetime(2017, 11, 14, 17, 0)
    end_date = datetime.datetime(2017, 11, 15, 23, 0)
    hashtag_1 = "FelizMartes" 
    #hashtag_2 = "BuiltWithPlanGrid"
    hashtag_2 = "youare"

    class Meta:
        model = HashtagBattle


class HashtagBattleFactoryTwo(factory.DjangoModelFactory):
    name = "Hashtag Battle One"
    start_date = datetime.datetime(2017, 11, 14, 17, 0)
    end_date = datetime.datetime(2017, 11, 14, 23, 0)
    hashtag_1 = "FelizMartes" 
    #hashtag_2 = "BuiltWithPlanGrid"
    hashtag_2 = "youare"

    class Meta:
        model = HashtagBattle
