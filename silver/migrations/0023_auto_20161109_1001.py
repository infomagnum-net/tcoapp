# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0022_auto_20161109_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rds',
            name='EndingRange',
            field=models.IntegerField(help_text=b'Please enterEndingRange ', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rds',
            name='Enhanced_Networking_Supported',
            field=models.CharField(help_text=b'Please enter Enhanced_Networking_Supported', max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rds',
            name='StartingRange',
            field=models.IntegerField(help_text=b'Please enter StartingRange ', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rds',
            name='engine_code',
            field=models.IntegerField(help_text=b'Please enter engine_code ', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rds',
            name='unit',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
