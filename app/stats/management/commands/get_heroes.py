import json
import logging
import os

import opendota
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = opendota.OpenDota(
            data_dir=os.path.join(settings.BASE_DIR, 'data', 'dota2'))

        heroes = client.get_heroes()

        print('Done!')
