# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcoapp', '0009_architecturetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='architecture',
            name='archtype',
            field=models.ForeignKey(blank=True, to='tcoapp.ArchitectureType', null=True),
        ),
    ]
