# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0033_auto_20161110_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Architecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('architecture_img', models.ImageField(null=True, upload_to=b'architectures', blank=True)),
                ('architecture_name', models.ForeignKey(to='silver.ProductCode')),
            ],
        ),
        migrations.CreateModel(
            name='ArchitectureType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archtype', models.CharField(unique=True, max_length=15, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureArchitecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_img', models.ImageField(null=True, upload_to=b'architectures/features/', blank=True)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('architecture_id', models.ForeignKey(to='silver.Architecture')),
                ('architecture_name', models.ForeignKey(to='silver.ProductCode')),
            ],
        ),
        migrations.AddField(
            model_name='architecture',
            name='archtype',
            field=models.ForeignKey(blank=True, to='silver.ArchitectureType', null=True),
        ),
    ]
