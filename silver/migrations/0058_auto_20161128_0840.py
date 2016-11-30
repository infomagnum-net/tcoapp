# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0057_auto_20161125_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_architecture',
            name='architecture_name',
            field=models.ForeignKey(to='silver.ProductCode', blank=True),
        ),
    ]
