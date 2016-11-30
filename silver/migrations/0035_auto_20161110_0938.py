# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0034_auto_20161110_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='architecture',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='featurearchitecture',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
