# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0032_userarchitectures'),
    ]

    operations = [
        migrations.AddField(
            model_name='userarchitectures',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 10, 6, 58, 4, 884573, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userarchitectures',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 10, 6, 58, 10, 564540, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
