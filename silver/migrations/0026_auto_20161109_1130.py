# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0025_auto_20161109_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s3storage',
            name='Availability',
            field=models.CharField(help_text=b'Please enter operation', max_length=200, null=True, blank=True),
        ),
    ]
