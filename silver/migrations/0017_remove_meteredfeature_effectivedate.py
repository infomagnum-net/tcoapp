# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0016_auto_20161104_0504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meteredfeature',
            name='EffectiveDate',
        ),
    ]
