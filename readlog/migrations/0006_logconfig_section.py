# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0005_auto_20150815_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='logconfig',
            name='section',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
