# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0020_remove_meteredfeature_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='RDS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('termstype', models.CharField(help_text=b'Please enter Termstype', max_length=200, null=True, blank=True)),
                ('PriceDescription', models.TextField(null=True, blank=True)),
                ('EffectiveDate', models.CharField(help_text=b'EffectiveDate', max_length=200, null=True, blank=True)),
                ('unit', models.CharField(max_length=20)),
                ('price_per_unit', models.DecimalField(help_text=b'The price per unit.', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('currency', models.CharField(help_text=b'Please enter currency', max_length=200, null=True, blank=True)),
                ('LeaseContractLength', models.CharField(help_text=b'Please enter LeaseContractLength', max_length=200, null=True, blank=True)),
                ('PurchaseOption', models.CharField(help_text=b'Please enter PurchaseOption', max_length=200, null=True, blank=True)),
                ('OfferingClass', models.CharField(help_text=b'Please enter OfferingClass', max_length=200, null=True, blank=True)),
                ('Product_Family', models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True)),
                ('StartingRange', models.IntegerField(null=True, blank=True)),
                ('EndingRange', models.IntegerField(null=True, blank=True)),
                ('RelatedTo', models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True)),
                ('serviceCode', models.CharField(help_text=b'Please enter serviceCode', max_length=200, null=True, blank=True)),
                ('Location_Type', models.CharField(help_text=b'Please enter Location Type', max_length=200, null=True, blank=True)),
                ('region', models.CharField(help_text=b'Please enter Region name', max_length=200, null=True, blank=True)),
                ('Instance_Type', models.CharField(help_text=b'Please enter Instance Type', max_length=200, null=True, blank=True)),
                ('Current_Generation', models.CharField(help_text=b'Please enter Current Generation', max_length=200, null=True, blank=True)),
                ('Instance_Family', models.CharField(help_text=b'Please enter Instance Family', max_length=200, null=True, blank=True)),
                ('vCPU', models.CharField(help_text=b'Please enter vCPU', max_length=200, null=True, blank=True)),
                ('Physical_Processor', models.CharField(help_text=b'Please enter Physical Processor', max_length=200, null=True, blank=True)),
                ('Clock_Speed', models.CharField(help_text=b'Please enter Clock Speed', max_length=200, null=True, blank=True)),
                ('Memory', models.CharField(help_text=b'Please enter Memory', max_length=200, null=True, blank=True)),
                ('Processor_Architecture', models.CharField(help_text=b'Please enter Processor Architecture', max_length=200, null=True, blank=True)),
                ('Storage', models.CharField(help_text=b'Please enter Storage', max_length=200, null=True, blank=True)),
                ('Network_Performance', models.CharField(help_text=b'Please enter Network Performance', max_length=200, null=True, blank=True)),
                ('Engine_Code', models.IntegerField(null=True, blank=True)),
                ('Database_Engine', models.CharField(help_text=b'Please enter  Database_Engine', max_length=200, null=True, blank=True)),
                ('Database_Edition', models.CharField(help_text=b'Please enter Database_Edition', max_length=200, null=True, blank=True)),
                ('License_Model', models.CharField(help_text=b'Please enter License_Model', max_length=200, null=True, blank=True)),
                ('Deployment_Option', models.CharField(help_text=b'Please enter Deployment_Option', max_length=200, null=True, blank=True)),
                ('Transfer_Type', models.CharField(help_text=b'Please enter Transfer_Type', max_length=200, null=True, blank=True)),
                ('From_Location', models.CharField(help_text=b'Please enter From_Location', max_length=200, null=True, blank=True)),
                ('From_Location_Type', models.CharField(help_text=b'Please enter From_Location_Type', max_length=200, null=True, blank=True)),
                ('To_Location', models.CharField(help_text=b'Please enter To_Location', max_length=200, null=True, blank=True)),
                ('To_Location_Type', models.CharField(help_text=b'Please enter To_Location_Type', max_length=200, null=True, blank=True)),
                ('usageType', models.CharField(help_text=b'Please enter usageType', max_length=200, null=True, blank=True)),
                ('operation', models.CharField(help_text=b'Please enter operation', max_length=200, null=True, blank=True)),
                ('Dedicated_EBS_Throughput', models.CharField(help_text=b'Please enter Dedicated_EBS_Throughput', max_length=200, null=True, blank=True)),
                ('Enhanced_Networking_Supported', models.CharField(help_text=b'Please enter Enhanced_Networking_Supported', max_length=200, null=True, blank=True)),
                ('Processor_Features', models.CharField(help_text=b'Please enter Processor_Features', max_length=200, null=True, blank=True)),
            ],
        ),
    ]
