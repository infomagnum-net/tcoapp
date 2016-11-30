# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0027_auto_20161109_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s3storage',
            name='Durability',
            field=models.CharField(help_text=b'Durability', max_length=200, null=True, blank=True),
        ),
    ]
