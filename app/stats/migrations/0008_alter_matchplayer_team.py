# Generated by Django 3.2 on 2021-11-03 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_auto_20211103_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchplayer',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.team', to_field='dota_id'),
        ),
    ]