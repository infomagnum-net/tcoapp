# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcoapp', '0007_auto_20161024_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='architecture',
            name='architecture_name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='featurearchitecture',
            name='architecture_name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
