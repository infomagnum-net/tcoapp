# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0031_auto_20161110_0556'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserArchitectures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text=b'username', max_length=200, null=True, blank=True)),
                ('arch_name', models.CharField(help_text=b'Architecture Name', max_length=200, null=True, blank=True)),
                ('price', models.DecimalField(help_text=b'price', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
    ]
