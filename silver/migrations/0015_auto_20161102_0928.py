# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0014_meteredfeature_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteredfeature',
            name='EBS_volume',
            field=models.IntegerField(help_text=b'Please enter EBS Volume ', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Elastic_IP',
            field=models.CharField(help_text=b'Please enter Elastic IP', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='ostype',
            field=models.CharField(help_text=b'Please enter OS Type', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meteredfeature',
            name='region',
            field=models.CharField(help_text=b'Please enter Region name', max_length=200, null=True, blank=True),
        ),
    ]
