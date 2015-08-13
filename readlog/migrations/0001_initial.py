# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BadBotsIp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('date_time', models.DateTimeField()),
                ('method', models.CharField(max_length=256)),
                ('endpoint', models.CharField(max_length=256)),
                ('protocol', models.CharField(max_length=256)),
                ('response_code', models.CharField(max_length=256)),
                ('content_size', models.CharField(max_length=256)),
                ('user_agents', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='GoodBots',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('date_time', models.DateTimeField()),
                ('method', models.CharField(max_length=256)),
                ('endpoint', models.CharField(max_length=256)),
                ('protocol', models.CharField(max_length=256)),
                ('response_code', models.CharField(max_length=256)),
                ('content_size', models.CharField(max_length=256)),
                ('user_agents', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='LogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('client_id', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=100)),
                ('date_time', models.DateTimeField()),
                ('method', models.CharField(max_length=256)),
                ('endpoint', models.CharField(max_length=256)),
                ('protocol', models.CharField(max_length=256)),
                ('response_code', models.CharField(max_length=256)),
                ('content_size', models.CharField(max_length=256)),
                ('user_agents', models.CharField(default=b'', max_length=256)),
                ('mobile', models.IntegerField(default=0)),
                ('user_agents_flag', models.IntegerField(default=0)),
            ],
        ),
    ]
