# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0052_auto_20161125_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='product_price',
            field=models.CharField(default=b'<property object at 0x7f0bb88fb7e0>', help_text=b'Display name of the plan.', max_length=200),
        ),
    ]
