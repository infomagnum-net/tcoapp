# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcoapp', '0004_architecture_architecture_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='architecture',
            name='architecture_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
