# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0006_logconfig_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature_vector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('no_of_requests', models.FloatField(default=0)),
                ('no_of_sections', models.FloatField(default=0)),
                ('avg_session_time', models.FloatField(default=0)),
                ('hits_per_session', models.FloatField(default=0)),
                ('time_bw_requests', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LogConfig_test',
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
                ('section', models.CharField(default=b'', max_length=256)),
            ],
        ),
    ]
