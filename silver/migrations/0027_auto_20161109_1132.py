# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0026_auto_20161109_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s3storage',
            name='Availability',
            field=models.CharField(help_text=b'Availability', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='s3storage',
            name='Durability',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
        ),
    ]
