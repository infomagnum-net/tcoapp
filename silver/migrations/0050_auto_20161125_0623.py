# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0049_auto_20161116_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='balancer_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='instance_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='rds_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s3_count',
            field=models.IntegerField(default=0),
        ),
    ]
