# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0018_meteredfeature_effectivedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteredfeature',
            name='Location',
            field=models.CharField(help_text=b'Please enter Location', max_length=200, null=True, blank=True),
        ),
    ]
