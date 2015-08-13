# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0002_auto_20150806_2050'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('Description', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Description', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Suspicious',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('Description', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Unknown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=100)),
                ('Description', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='badbotsip',
            name='Description',
            field=models.CharField(default=b'', max_length=256),
        ),
        migrations.AddField(
            model_name='goodbots',
            name='Description',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
