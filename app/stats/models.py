from django.db import models
import autoslug


class Player(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveBigIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')


class LeagueSeason(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')


class Match(models.Model):
    dota_id = models.PositiveBigIntegerField(unique=True)
    did_radiant_win = models.BooleanField()
    duration_seconds = models.PositiveSmallIntegerField()
    end_datetime = models.DateTimeField()
    avg_imp = models.PositiveSmallIntegerField()  # Individual Player Performance, impact
    radiant_team = models.ForeignKey(Team, to_field='dota_id', on_delete=models.CASCADE,
                                     related_name='matches_radiant')
    dire_team = models.ForeignKey(Team, to_field='dota_id', on_delete=models.CASCADE,
                                  related_name='matches_dire')
    league_id = models.ForeignKey(LeagueSeason, to_field='dota_id', on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, through='MatchPlayer')


class Hero(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveSmallIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')


class MatchPlayer(models.Model):
    match = models.ForeignKey(Match, to_field='dota_id', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, to_field='dota_id', on_delete=models.CASCADE)
    hero = models.ForeignKey(Hero, to_field='dota_id', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, to_field='dota_id', on_delete=models.CASCADE)

    is_radiant = models.BooleanField()
    is_victory = models.BooleanField()
    num_kills = models.PositiveSmallIntegerField()
    num_deaths = models.PositiveSmallIntegerField()
    num_assists = models.PositiveSmallIntegerField()
    num_lasthits = models.PositiveSmallIntegerField()
    num_denies = models.PositiveSmallIntegerField()
    gpm = models.PositiveIntegerField()
    xpm = models.PositiveIntegerField()
    level = models.PositiveSmallIntegerField()
    gold = models.PositiveIntegerField()
    networth = models.PositiveIntegerField()
    gold_spent = models.PositiveIntegerField()
    hero_damage = models.PositiveIntegerField()
    tower_damage = models.PositiveIntegerField()
    lane = models.PositiveSmallIntegerField()
    role = models.PositiveSmallIntegerField()
    imp = models.PositiveSmallIntegerField()  # Individual Player Performance, impact
    award = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('player', 'match')
        ordering = ('-match__end_datetime', 'is_radiant')
