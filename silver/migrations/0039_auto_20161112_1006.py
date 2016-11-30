# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0038_laoadbalencer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LaoadBalencer',
            new_name='LoadBalencer',
        ),
    ]
