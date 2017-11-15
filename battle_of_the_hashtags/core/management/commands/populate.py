from django.core.management.base import BaseCommand
from django.core import management

from core.factories import HashtagBattleFactory


class Command(BaseCommand):
    def handle(self, **options):
        hastag_battle_factory_1 = HashtagBattleFactoryOne()
        hastag_battle_factory_2 = HashtagBattleFactoryTwo()
