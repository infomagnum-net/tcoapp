# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0055_auto_20161125_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='product_price',
        ),
        migrations.AddField(
            model_name='plan',
            name='balancer_price',
            field=models.CharField(max_length=4, blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='instance_price',
            field=models.CharField(max_length=4, blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='rds_price',
            field=models.CharField(max_length=4, blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='s3_price',
            field=models.CharField(max_length=4, blank=True),
        ),
    ]
