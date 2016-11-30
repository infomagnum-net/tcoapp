# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0012_region'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name_plural': 'Region'},
        ),
    ]
