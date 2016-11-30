# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0021_rds'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rds',
            old_name='Engine_Code',
            new_name='engine_code',
        ),
    ]
