# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0039_auto_20161112_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadbalencer',
            name='product_code',
            field=models.ForeignKey(help_text=b'The product code for this plan.', to='silver.ProductCode'),
        ),
    ]
