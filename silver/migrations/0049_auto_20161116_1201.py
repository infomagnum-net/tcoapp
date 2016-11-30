# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0048_customer_architecture_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='architecture_img',
            new_name='profile_img',
        ),
    ]
