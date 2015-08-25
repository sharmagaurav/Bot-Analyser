# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0009_badbotsip_test_goodbots_test_logconfig_test_dump_suspicious_test_training_centroids'),
    ]

    operations = [
        migrations.AddField(
            model_name='training_centroids',
            name='distance',
            field=models.FloatField(default=0.0),
        ),
    ]
