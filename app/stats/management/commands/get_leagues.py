import json
import logging
import os
from urllib.parse import urlsplit

import opendota
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = opendota.OpenDota(
            data_dir=os.path.join(settings.BASE_DIR, 'data', 'opendota'))

        url = "/leagues"
        filename = "leagues.json"
        path = os.path.join(client.data_dir, filename)

        json_data = client.get(url, filename=None)

        with open(path, 'w', encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False)

        print('Done!')
