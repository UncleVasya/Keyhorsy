import json
import logging
import os

import opendota
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction

from app.stats.models import Hero, Player


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('player', type=str)
        parser.add_argument('hero', type=str)

    def handle(self, *args, **options):
        player = options['player']
        hero = options['hero']

        # lookup player and hero names in db
        player = Player.objects.filter(name__istartswith=player).first()
        hero = Hero.objects.filter(name__istartswith=hero).first()

        # filter player matches on a hero
        matches = player.matchplayer_set.filter(hero=hero)

        wins = matches.filter(is_victory=True).count()
        losses = matches.filter(is_victory=False).count()

        print(f'{player} on {hero}: {wins}-{losses}')
