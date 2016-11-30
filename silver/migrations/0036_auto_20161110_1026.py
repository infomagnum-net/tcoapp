# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0035_auto_20161110_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing_Architecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('architecture_img', models.ImageField(null=True, upload_to=b'architectures', blank=True)),
                ('description', models.TextField(blank=True)),
                ('architecture_name', models.ForeignKey(to='silver.ProductCode')),
            ],
        ),
        migrations.CreateModel(
            name='Billing_FeatureArchitecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_img', models.ImageField(null=True, upload_to=b'architectures/features/', blank=True)),
                ('description', models.TextField(blank=True)),
                ('architecture_id', models.ForeignKey(to='silver.Billing_Architecture')),
                ('architecture_name', models.ForeignKey(to='silver.ProductCode')),
            ],
        ),
        migrations.RenameModel(
            old_name='ArchitectureType',
            new_name='Billing_ArchitectureType',
        ),
        migrations.RemoveField(
            model_name='architecture',
            name='architecture_name',
        ),
        migrations.RemoveField(
            model_name='architecture',
            name='archtype',
        ),
        migrations.RemoveField(
            model_name='featurearchitecture',
            name='architecture_id',
        ),
        migrations.RemoveField(
            model_name='featurearchitecture',
            name='architecture_name',
        ),
        migrations.DeleteModel(
            name='Architecture',
        ),
        migrations.DeleteModel(
            name='FeatureArchitecture',
        ),
        migrations.AddField(
            model_name='billing_architecture',
            name='archtype',
            field=models.ForeignKey(blank=True, to='silver.Billing_ArchitectureType', null=True),
        ),
    ]
