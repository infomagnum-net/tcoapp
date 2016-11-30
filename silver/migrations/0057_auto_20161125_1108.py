# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0056_auto_20161125_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='balancer_price',
            field=models.DecimalField(blank=True, max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='plan',
            name='instance_price',
            field=models.DecimalField(blank=True, max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='plan',
            name='rds_price',
            field=models.DecimalField(blank=True, max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s3_price',
            field=models.DecimalField(blank=True, max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
