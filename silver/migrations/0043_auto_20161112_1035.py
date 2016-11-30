# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0042_auto_20161112_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='metered_features',
            field=models.ManyToManyField(default=b'No Value', help_text=b"A list of the plan's metered features.", related_name='sasas', to='silver.MeteredFeature', blank=True),
        ),
    ]
