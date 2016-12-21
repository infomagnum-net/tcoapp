# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0059_auto_20161128_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing_architecture',
            name='apptype',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AddField(
            model_name='billing_featurearchitecture',
            name='apptype',
            field=models.CharField(max_length=150, blank=True),
        ),
    ]
