import json
import logging
import os

import opendota
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction

from app.stats.models import Hero


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = opendota.OpenDota(
            data_dir=os.path.join(settings.BASE_DIR, 'data', 'dota2'))

        heroes = client.get_heroes()

        with transaction.atomic():
            for hero in heroes:
                Hero.objects.get_or_create(
                    dota_id=hero['id'],
                    defaults={
                        'name': hero['localized_name'],
                    },
                )

        print('Done!')
