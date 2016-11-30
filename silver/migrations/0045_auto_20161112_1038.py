# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0044_auto_20161112_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='LoadBalencer_metered',
            field=models.ManyToManyField(default=b'No Value', help_text=b"A list of the plan's metered features.", to='silver.LoadBalencer', blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='balancer_count',
            field=models.IntegerField(default=1),
        ),
    ]
