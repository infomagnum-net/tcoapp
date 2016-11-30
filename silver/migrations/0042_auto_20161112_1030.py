# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0041_auto_20161112_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='metered_features',
            field=models.ManyToManyField(default=b'No Value', help_text=b"A list of the plan's metered features.", to='silver.MeteredFeature', blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='rds_metered_feature',
            field=models.ManyToManyField(default=b'No Value', help_text=b"A list of the plan's RDS metered features.", to='silver.RDS', blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s3_metered_features',
            field=models.ManyToManyField(default=b'No Value', help_text=b"A list of the plan's S3 metered features.", to='silver.S3Storage', blank=True),
        ),
    ]
