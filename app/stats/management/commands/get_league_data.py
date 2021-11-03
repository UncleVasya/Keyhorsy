import json
import logging
import os
import opendota
from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from django.utils.datetime_safe import datetime

from app.stats.models import LeagueSeason, Team, Match, MatchPlayer, Player

DATA_DIR = os.path.join(settings.BASE_DIR, 'data', 'dota2')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('league', type=int)

    def handle(self, *args, **options):
        league_id = options['league']
        # logging.basicConfig(level=logging.INFO)
        # TODO: if we have no heroes in db, execute get_heroes script

        # save league info
        league = Command.get_league_info(league_id)
        league, _ = LeagueSeason.objects.get_or_create(
            dota_id=league['leagueid'],
            defaults={
                'name': league['name'],
            },
        )

        matches = Command.get_league_matches(league_id)

        # save all involved players and teams
        teams = set()
        players = set()
        for m in matches:
            teams.update([m['radiantTeamId'], m['direTeamId']])
            players.update(p['steamAccountId'] for p in m['players'])

        teams = Command.get_teams(teams)
        Command.save_teams(teams)

        players = Command.get_players(players)
        Command.save_players(players)

        # now when we have players and teams data in db,
        # we can save matches data
        Command.save_matches(matches)

        print('Done!')

    @staticmethod
    def get_teams(team_ids):
        # remove invalid ids that happen when people forget to set teams
        team_ids = [t for t in team_ids if t > 0]

        client = opendota.OpenDota(
            api_url='https://api.stratz.com/api/v1',
            data_dir=DATA_DIR)

        teams = []
        for team in team_ids:
            team = client.get(url=f'/team/{team}',
                              filename=f'team_{team}.json')
            teams.append(team)

        return teams

    @staticmethod
    def get_players(player_ids):
        client = opendota.OpenDota(data_dir=DATA_DIR)
        return [client.get_player(player) for player in player_ids]

    @staticmethod
    def save_teams(teams):
        with transaction.atomic():
            for team in teams:
                Team.objects.get_or_create(
                    dota_id=team['id'],
                    defaults={
                        'name': team['name'],
                    },
                )

    @staticmethod
    def save_players(players):
        with transaction.atomic():
            for player in players:
                Player.objects.get_or_create(
                    dota_id=player['profile']['account_id'],
                    defaults={
                        'name': player['profile']['personaname'],
                    },
                )

    @staticmethod
    def save_matches(matches):
        with transaction.atomic():
            for match in matches:
                _, created = Match.objects.get_or_create(
                    dota_id=match['id'],
                    defaults={
                        'did_radiant_win': match['didRadiantWin'],
                        'duration_seconds': match['durationSeconds'],
                        'end_datetime': datetime.fromtimestamp(match['endDateTime']),
                        'avg_imp': match.get('avgImp', None),
                        'radiant_team_id': match['radiantTeamId'] if match['radiantTeamId'] > 0 else None,
                        'dire_team_id': match['direTeamId'] if match['direTeamId'] > 0 else None,
                        'league_id': match['leagueId'],
                    },
                )
                if created:
                    for player in match['players']:
                        team_id = match['radiantTeamId'] if player['isRadiant'] else match['direTeamId']
                        team_id = team_id if team_id > 0 else None
                        MatchPlayer.objects.create(
                            match_id=match['id'],
                            player_id=player['steamAccountId'],
                            hero_id=player['heroId'],
                            team_id=team_id,
                            is_radiant=player['isRadiant'],
                            is_victory=player['isVictory'],
                            num_kills=player['numKills'],
                            num_deaths=player['numDeaths'],
                            num_assists=player['numAssists'],
                            num_lasthits=player['numLastHits'],
                            num_denies=player['numDenies'],
                            gpm=player['goldPerMinute'],
                            xpm=player['experiencePerMinute'],
                            level=player['level'],
                            gold=player['gold'],
                            networth=player['networth'],
                            gold_spent=player['goldSpent'],
                            hero_damage=player['heroDamage'],
                            tower_damage=player['towerDamage'],
                            lane=player.get('lane', None),
                            role=player.get('role', None),
                            imp=player.get('imp', None),
                            award=player.get('award', None),
                        )

    @staticmethod
    def get_league_matches(league_id):
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
            matches = Command.download_league_matches(league_id)
        else:
            print(f'newest match id: {matches[0]["id"]}')
            new_matches = Command.download_league_matches(league_id, stop_at=matches[0]['id'])
            matches = new_matches + matches

        print(f'matches after update: {len(matches)}')

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(matches, f, ensure_ascii=False)

        return matches

    @staticmethod
    def get_league_info(league_id):
        client = opendota.OpenDota(data_dir=DATA_DIR)
        return client.get_league(league_id)

    @staticmethod
    def download_league_matches(league_id, stop_at=None):
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
            except Exception as e:
                print(e)
                break

        return matches

