# Generated by Django 3.2 on 2021-11-03 14:15

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('dota_id', models.PositiveSmallIntegerField(unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('dota_id', models.PositiveIntegerField(unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dota_id', models.PositiveBigIntegerField(unique=True)),
                ('did_radiant_win', models.BooleanField()),
                ('duration_seconds', models.PositiveSmallIntegerField()),
                ('end_datetime', models.DateTimeField()),
                ('avg_imp', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('dota_id', models.PositiveBigIntegerField(unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('dota_id', models.PositiveIntegerField(unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='MatchPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_radiant', models.BooleanField()),
                ('is_victory', models.BooleanField()),
                ('num_kills', models.PositiveSmallIntegerField()),
                ('num_deaths', models.PositiveSmallIntegerField()),
                ('num_assists', models.PositiveSmallIntegerField()),
                ('num_lasthits', models.PositiveSmallIntegerField()),
                ('num_denies', models.PositiveSmallIntegerField()),
                ('gpm', models.PositiveIntegerField()),
                ('xpm', models.PositiveIntegerField()),
                ('level', models.PositiveSmallIntegerField()),
                ('gold', models.PositiveIntegerField()),
                ('networth', models.PositiveIntegerField()),
                ('gold_spent', models.PositiveIntegerField()),
                ('hero_damage', models.PositiveIntegerField()),
                ('tower_damage', models.PositiveIntegerField()),
                ('lane', models.PositiveSmallIntegerField()),
                ('role', models.PositiveSmallIntegerField()),
                ('imp', models.PositiveSmallIntegerField()),
                ('award', models.PositiveSmallIntegerField()),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.hero', to_field='dota_id')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.match', to_field='dota_id')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.player', to_field='dota_id')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.team', to_field='dota_id')),
            ],
            options={
                'ordering': ('-match__end_datetime', 'is_radiant'),
                'unique_together': {('player', 'match')},
            },
        ),
        migrations.AddField(
            model_name='match',
            name='dire_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_dire', to='stats.team', to_field='dota_id'),
        ),
        migrations.AddField(
            model_name='match',
            name='league_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.leagueseason', to_field='dota_id'),
        ),
        migrations.AddField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(through='stats.MatchPlayer', to='stats.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='radiant_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_radiant', to='stats.team', to_field='dota_id'),
        ),
    ]