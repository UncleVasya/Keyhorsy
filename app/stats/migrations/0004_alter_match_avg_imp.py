# Generated by Django 3.2 on 2021-11-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_alter_matchplayer_imp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='avg_imp',
            field=models.SmallIntegerField(),
        ),
    ]
