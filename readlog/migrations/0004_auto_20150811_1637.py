# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0003_auto_20150809_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='badbotsip',
            name='date_time',
            field=models.DateTimeField(default=b'1900-01-01 00:00:00'),
        ),
        migrations.AddField(
            model_name='goodbots',
            name='date_time',
            field=models.DateTimeField(default=b'1900-01-01 00:00:00'),
        ),
        migrations.AddField(
            model_name='goodusers',
            name='date_time',
            field=models.DateTimeField(default=b'1900-01-01 00:00:00'),
        ),
        migrations.AddField(
            model_name='suspicious',
            name='date_time',
            field=models.DateTimeField(default=b'1900-01-01 00:00:00'),
        ),
        migrations.AddField(
            model_name='unknown',
            name='date_time',
            field=models.DateTimeField(default=b'1900-01-01 00:00:00'),
        ),
    ]
