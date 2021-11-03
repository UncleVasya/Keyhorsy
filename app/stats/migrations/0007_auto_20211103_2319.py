# Generated by Django 3.2 on 2021-11-03 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20211103_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='dire_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches_dire', to='stats.team', to_field='dota_id'),
        ),
        migrations.AlterField(
            model_name='match',
            name='radiant_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches_radiant', to='stats.team', to_field='dota_id'),
        ),
    ]
