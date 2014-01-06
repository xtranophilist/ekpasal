__author__ = 'xtranophilist'

from store.aggregators.yeskantipur import Yeskantipur
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        yk = Yeskantipur()
        yk.mine()



