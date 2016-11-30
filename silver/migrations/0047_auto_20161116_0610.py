# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0046_customer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='facebook',
            field=models.CharField(help_text=b"facebook address (eg. 'user@facebook').", max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='skype',
            field=models.CharField(help_text=b"twitter address (eg. 'user@skype').", max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='twitter',
            field=models.CharField(help_text=b"twitter address (eg. 'user@twitter').", max_length=64, null=True, blank=True),
        ),
    ]
