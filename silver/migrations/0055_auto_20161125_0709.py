# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0054_auto_20161125_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='product_price',
            field=models.CharField(default=b'<property object at 0x7f38fe6677e0>', help_text=b'Display name of the plan.', max_length=200, blank=True),
        ),
    ]
