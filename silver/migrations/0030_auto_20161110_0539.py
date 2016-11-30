# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0029_plan_ec2count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='EC2count',
            new_name='instance_count',
        ),
    ]
