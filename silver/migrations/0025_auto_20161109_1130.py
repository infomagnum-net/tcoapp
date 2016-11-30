# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0024_auto_20161109_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rds',
            name='price_per_unit',
            field=models.DecimalField(help_text=b'The price per unit.', max_digits=19, decimal_places=10, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='s3storage',
            name='Availability',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
        ),
        migrations.AlterField(
            model_name='s3storage',
            name='Durability',
            field=models.CharField(help_text=b'Please enter operation', max_length=200, null=True, blank=True),
        ),
    ]
