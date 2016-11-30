# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0019_meteredfeature_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meteredfeature',
            name='Location',
        ),
    ]
