# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0050_auto_20161125_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(default=20, help_text=b'The amount in the specified currency to be charged on the interval specified.', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
