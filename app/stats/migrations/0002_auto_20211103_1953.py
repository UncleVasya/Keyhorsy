# Generated by Django 3.2 on 2021-11-03 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-end_datetime']},
        ),
        migrations.AlterModelOptions(
            name='matchplayer',
            options={'ordering': ['-match__end_datetime', 'is_radiant']},
        ),
        migrations.RenameField(
            model_name='match',
            old_name='league_id',
            new_name='league',
        ),
    ]
