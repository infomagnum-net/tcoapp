# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0028_auto_20161110_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='EC2count',
            field=models.IntegerField(default=1),
        ),
    ]
