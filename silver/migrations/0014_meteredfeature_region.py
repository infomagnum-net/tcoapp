# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0013_auto_20161102_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteredfeature',
            name='region',
            field=models.ForeignKey(blank=True, to='silver.Region', null=True),
        ),
    ]
