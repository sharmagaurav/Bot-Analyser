# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0004_auto_20150811_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='badbotsip',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='goodbots',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='goodusers',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='suspicious',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='unknown',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]
