# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0030_auto_20161110_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='rds_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='plan',
            name='rds_metered_feature',
            field=models.ManyToManyField(help_text=b"A list of the plan's RDS metered features.", to='silver.RDS', blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='s3_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='plan',
            name='s3_metered_features',
            field=models.ManyToManyField(help_text=b"A list of the plan's S3 metered features.", to='silver.S3Storage', blank=True),
        ),
    ]
