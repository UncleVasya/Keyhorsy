from django.contrib import admin

from app.stats.models import Hero, Player, Match, MatchPlayer, Team, LeagueSeason


class HeroAdmin(admin.ModelAdmin):
    model = Hero
    list_display = ['dota_id', 'name']


class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = ['dota_id', 'name']


class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ['dota_id']


class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['dota_id', 'name']


class LeagueSeasonAdmin(admin.ModelAdmin):
    model = LeagueSeason
    list_display = ['dota_id', 'name']


class MatchPlayerAdmin(admin.ModelAdmin):
    model = MatchPlayer


admin.site.register(Hero, HeroAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchPlayer, MatchPlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(LeagueSeason, LeagueSeasonAdmin)
