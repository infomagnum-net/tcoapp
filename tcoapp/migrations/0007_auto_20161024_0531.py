# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcoapp', '0006_auto_20161019_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('stripe_id', models.IntegerField()),
                ('plan_type', models.CharField(max_length=100, blank=True)),
                ('card_number', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='iam_access_key',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='iam_secret_key',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='iam_status',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='reg_cnrrm_code',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
