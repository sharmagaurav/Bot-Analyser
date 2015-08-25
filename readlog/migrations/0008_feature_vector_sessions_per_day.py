# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readlog', '0007_feature_vector_logconfig_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature_vector',
            name='sessions_per_day',
            field=models.FloatField(default=0),
        ),
    ]
