# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcoapp', '0011_userinfo_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='profile_img',
            field=models.ImageField(null=True, upload_to='architectures', blank=True),
        ),
    ]
