import json
import logging
import os
import time

import opendota
from django.conf import settings
from django.core.management import BaseCommand

DATA_DIR = os.path.join(settings.BASE_DIR, 'data', 'dota2')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('league', type=int)

    def handle(self, *args, **options):
        # logging.basicConfig(level=logging.INFO)
        league_id = options['league']

        filename = f'league_{league_id}_matches.json'
        path = os.path.join(DATA_DIR, filename)
        matches = []

        # first check if we have some match data already
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding="utf-8") as f:
                    matches = json.load(f)
            except Exception:
                pass

        print(f'present matches: {len(matches)}')
        if len(matches) == 0:
            matches = self.get_league_matches(league_id)
        else:
            print(f'newest match id: {matches[0]["id"]}')
            new_matches = self.get_league_matches(league_id, stop_at=matches[0]['id'])
            matches = new_matches + matches

        print(f'matches after update: {len(matches)}')

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(matches, f, ensure_ascii=False)

    @staticmethod
    def get_league_matches(league_id, stop_at=None):
        client = opendota.OpenDota(
            api_url='https://api.stratz.com/api/v1',
            data_dir=DATA_DIR)

        take = 100
        matches = []
        # traverse league matches in chunks of 100
        while True:
            skip = len(matches)
            try:
                chunk = client.get(
                    url=f'/league/{league_id}/matches',
                    data={
                        'skip': skip,
                        'take': take,
                    })

                if stop_at:  # if we need only to update data with new matches
                    stop_index = next((i for i, x in enumerate(chunk) if x['id'] == stop_at), None)
                    if stop_index is not None:
                        chunk = chunk[:stop_index]

                matches += chunk
                print(f'matches downloaded: {len(matches)}')

                if not chunk or len(chunk) % take != 0:
                    break  # match list is over

                time.sleep(2)
            except Exception as e:
                print(e)
                break

        return matches