# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0045_auto_20161112_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.TextField(help_text=b"mobile no (eg. '9876543210').", max_length=64, null=True, blank=True),
        ),
    ]
