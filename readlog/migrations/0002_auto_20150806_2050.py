# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badbotsip',
            name='content_size',
        ),
        migrations.RemoveField(
            model_name='badbotsip',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='badbotsip',
            name='endpoint',
        ),
        migrations.RemoveField(
            model_name='badbotsip',
            name='method',
        ),
        migrations.RemoveField(
            model_name='badbotsip',
            name='protocol',
        ),
        migrations.RemoveField(
            model_name='badbotsip',
            name='response_code',
        ),
        migrations.RemoveField(
            model_name='badbotsip',
            name='user_agents',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='content_size',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='endpoint',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='method',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='protocol',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='response_code',
        ),
        migrations.RemoveField(
            model_name='goodbots',
            name='user_agents',
        ),
    ]
