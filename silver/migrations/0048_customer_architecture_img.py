# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0047_auto_20161116_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='architecture_img',
            field=models.ImageField(null=True, upload_to=b'profile-pics', blank=True),
        ),
    ]
