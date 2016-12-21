# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0060_auto_20161220_0549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing_architecture',
            name='apptype',
        ),
        migrations.RemoveField(
            model_name='billing_featurearchitecture',
            name='apptype',
        ),
        migrations.AddField(
            model_name='billing_architecture',
            name='apptype_img',
            field=models.ImageField(null=True, upload_to=b'apptype', blank=True),
        ),
        migrations.AddField(
            model_name='billing_featurearchitecture',
            name='apptype_img',
            field=models.ImageField(null=True, upload_to=b'apptype', blank=True),
        ),
    ]
