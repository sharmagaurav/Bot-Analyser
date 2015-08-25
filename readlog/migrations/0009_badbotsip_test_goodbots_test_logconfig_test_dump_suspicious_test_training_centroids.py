# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0008_feature_vector_sessions_per_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadBotsIp_test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('Description', models.CharField(default=b'', max_length=256)),
                ('date_time', models.DateTimeField(default=b'1900-01-01 00:00:00')),
                ('hits', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GoodBots_test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('Description', models.CharField(default=b'', max_length=256)),
                ('date_time', models.DateTimeField(default=b'1900-01-01 00:00:00')),
                ('hits', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='logconfig_test_dump',
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
        migrations.CreateModel(
            name='Suspicious_test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('Description', models.CharField(default=b'', max_length=256)),
                ('date_time', models.DateTimeField(default=b'1900-01-01 00:00:00')),
                ('hits', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='training_centroids',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Description', models.CharField(max_length=256)),
                ('centroid1', models.FloatField(default=0.0)),
                ('centroid2', models.FloatField(default=0.0)),
                ('centroid3', models.FloatField(default=0.0)),
                ('count', models.IntegerField(default=0)),
                ('deviation', models.FloatField(default=0.0)),
            ],
        ),
    ]
