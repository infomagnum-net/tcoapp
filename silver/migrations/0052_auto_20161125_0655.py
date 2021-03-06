# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0051_auto_20161125_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(help_text=b'The amount in the specified currency to be charged on the interval specified.', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
