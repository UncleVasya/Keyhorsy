from django.db import models
import autoslug


class Player(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveBigIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class LeagueSeason(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class Match(models.Model):
    dota_id = models.PositiveBigIntegerField(unique=True)
    did_radiant_win = models.BooleanField()
    duration_seconds = models.PositiveSmallIntegerField()
    end_datetime = models.DateTimeField()
    avg_imp = models.SmallIntegerField(null=True, blank=True)  # Individual Player Performance, impact

    radiant_team = models.ForeignKey(Team,
                                     to_field='dota_id',
                                     on_delete=models.CASCADE,
                                     related_name='matches_radiant',
                                     blank=True, null=True)  # sometimes people forget to set teams
    dire_team = models.ForeignKey(Team,
                                  to_field='dota_id',
                                  on_delete=models.CASCADE,
                                  related_name='matches_dire',
                                  blank=True, null=True)

    league = models.ForeignKey(LeagueSeason, to_field='dota_id', on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, through='MatchPlayer')

    class Meta:
        ordering = ['-end_datetime']


class Hero(models.Model):
    name = models.CharField(max_length=200, unique=True)
    dota_id = models.PositiveSmallIntegerField(unique=True)
    slug = autoslug.AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class MatchPlayer(models.Model):
    match = models.ForeignKey(Match, to_field='dota_id', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, to_field='dota_id', on_delete=models.CASCADE)
    hero = models.ForeignKey(Hero, to_field='dota_id', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, to_field='dota_id', on_delete=models.CASCADE,
                             blank=True, null=True)  # sometimes people forget to set teams

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
    lane = models.PositiveSmallIntegerField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(null=True, blank=True)
    imp = models.SmallIntegerField(null=True, blank=True)  # Individual Player Performance, impact
    award = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['player', 'match']
        ordering = ['-match__end_datetime', 'is_radiant']

    def __str__(self):
        return f'{self.player} | {self.hero}'
