# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcoapp', '0015_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
