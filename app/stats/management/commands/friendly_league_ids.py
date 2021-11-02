import csv
import json
import os
from django.conf import settings
from django.core.management import BaseCommand

"""
This script produces a list of RD2L / Clarity / Doghouse league ids for different seasons.
Output will be in friendly_league_ids.csv
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'data', 'dota2')

        # read leagues data gathered from opendota
        filename = 'leagues.json'
        path = os.path.join(data_dir, filename)
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding="utf-8") as f:
                    leagues = json.load(f)
            except Exception as e:
                print('Cannot load leagues data.')
                print(e)

        # filter friendly leagues
        good_names = ['rd2l', 'clarity', 'doghouse']
        leagues = [league for league in leagues if
                   any(name in league['name'].lower() for name in good_names)]

        # write csv
        filename = 'friendly_league_ids.csv'
        path = os.path.join(data_dir, filename)
        csv_columns = ['leagueid', 'name']
        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns,
                                    extrasaction='ignore', lineterminator='\n')
            writer.writeheader()
            for league in leagues:
                writer.writerow(league)

            # additional seasons found manually
            writer.writer.writerow([2350, "Redditors\' Dota 2 League"])
