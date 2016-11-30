# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import silver.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0037_auto_20161112_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaoadBalencer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(help_text=b'Please enter Region name', max_length=200, null=True, blank=True)),
                ('ostype', models.CharField(help_text=b'Please enter OS Type', max_length=200, null=True, blank=True)),
                ('name', models.CharField(help_text=b'The feature display name.', max_length=200, db_index=True)),
                ('unit', models.CharField(max_length=20)),
                ('price_per_unit', models.DecimalField(help_text=b'The price per unit.', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('included_units', models.DecimalField(help_text=b'The number of included units per plan interval.', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('included_units_during_trial', models.DecimalField(decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)], max_digits=19, blank=True, help_text=b'The number of included units during the trial period.', null=True)),
                ('EBS_volume', models.IntegerField(help_text=b'Please enter EBS Volume ', null=True, blank=True)),
                ('Elastic_IP', models.CharField(help_text=b'Please enter Elastic IP', max_length=200, null=True, blank=True)),
                ('termstype', models.CharField(help_text=b'Please enter Termstype', max_length=200, null=True, blank=True)),
                ('PriceDescription', models.TextField(null=True, blank=True)),
                ('EffectiveDate', models.CharField(help_text=b'EffectiveDate', max_length=200, null=True, blank=True)),
                ('currency', models.CharField(help_text=b'Please enter currency', max_length=200, null=True, blank=True)),
                ('LeaseContractLength', models.CharField(help_text=b'Please enter LeaseContractLength', max_length=200, null=True, blank=True)),
                ('PurchaseOption', models.CharField(help_text=b'Please enter PurchaseOption', max_length=200, null=True, blank=True)),
                ('OfferingClass', models.CharField(help_text=b'Please enter OfferingClass', max_length=200, null=True, blank=True)),
                ('Product_Family', models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True)),
                ('serviceCode', models.CharField(help_text=b'Please enter serviceCode', max_length=200, null=True, blank=True)),
                ('Location_Type', models.CharField(help_text=b'Please enter Location Type', max_length=200, null=True, blank=True)),
                ('Instance_Type', models.CharField(help_text=b'Please enter Instance Type', max_length=200, null=True, blank=True)),
                ('Current_Generation', models.CharField(help_text=b'Please enter Current Generation', max_length=200, null=True, blank=True)),
                ('Instance_Family', models.CharField(help_text=b'Please enter Instance Family', max_length=200, null=True, blank=True)),
                ('vCPU', models.CharField(help_text=b'Please enter vCPU', max_length=200, null=True, blank=True)),
                ('Physical_Processor', models.CharField(help_text=b'Please enter Physical Processor', max_length=200, null=True, blank=True)),
                ('Clock_Speed', models.CharField(help_text=b'Please enter Clock Speed', max_length=200, null=True, blank=True)),
                ('Memory', models.CharField(help_text=b'Please enter Memory', max_length=200, null=True, blank=True)),
                ('Storage', models.CharField(help_text=b'Please enter Storage', max_length=200, null=True, blank=True)),
                ('Network_Performance', models.CharField(help_text=b'Please enter Network Performance', max_length=200, null=True, blank=True)),
                ('Processor_Architecture', models.CharField(help_text=b'Please enter Processor Architecture', max_length=200, null=True, blank=True)),
                ('Storage_Media', models.CharField(help_text=b'Please enter Storage Media', max_length=200, null=True, blank=True)),
                ('Volume_Type', models.CharField(help_text=b'Please enter Volume Type', max_length=200, null=True, blank=True)),
                ('Max_Volume_Size', models.CharField(help_text=b'Please enter Max Volume Size', max_length=200, null=True, blank=True)),
                ('Max_IOPS_volume', models.CharField(help_text=b'Please enter Max IOPS_volume', max_length=200, null=True, blank=True)),
                ('Max_IOPS_Burst_Performance', models.CharField(help_text=b'Please enter Max_IOPS_Burst_Performance', max_length=200, null=True, blank=True)),
                ('Max_throughput_volume', models.CharField(help_text=b'Please enter Max_throughput_volume', max_length=200, null=True, blank=True)),
                ('Provisioned', models.CharField(help_text=b'Please enter Provisioned', max_length=200, null=True, blank=True)),
                ('Tenancy', models.CharField(help_text=b'Please enter Tenancy', max_length=200, null=True, blank=True)),
                ('EBS_Optimized', models.CharField(help_text=b'Please enter EBS_Optimize', max_length=200, null=True, blank=True)),
                ('Operating_System', models.CharField(help_text=b'Please enter Operating_System', max_length=200, null=True, blank=True)),
                ('License_Model', models.CharField(help_text=b'Please enter License_Model', max_length=200, null=True, blank=True)),
                ('Group', models.CharField(help_text=b'Please enter Group', max_length=200, null=True, blank=True)),
                ('Group_Description', models.CharField(help_text=b'Please enter Group_Description', max_length=200, null=True, blank=True)),
                ('Transfer_Type', models.CharField(help_text=b'Please enter Transfer_Type', max_length=200, null=True, blank=True)),
                ('From_Location', models.CharField(help_text=b'Please enter From_Location', max_length=200, null=True, blank=True)),
                ('From_Location_Type', models.CharField(help_text=b'Please enter From_Location_Type', max_length=200, null=True, blank=True)),
                ('To_Location', models.CharField(help_text=b'Please enter To_Location', max_length=200, null=True, blank=True)),
                ('To_Location_Type', models.CharField(help_text=b'Please enter To_Location_Type', max_length=200, null=True, blank=True)),
                ('usageType', models.CharField(help_text=b'Please enter usageType', max_length=200, null=True, blank=True)),
                ('operation', models.CharField(help_text=b'Please enter operation', max_length=200, null=True, blank=True)),
                ('Dedicated_EBS_Throughput', models.CharField(help_text=b'Please enter Dedicated_EBS_Throughput', max_length=200, null=True, blank=True)),
                ('Enhanced_Networking_Supported', models.CharField(help_text=b'Please enter Enhanced_Networking_Supported', max_length=200, null=True, blank=True)),
                ('GPU', models.CharField(help_text=b'Please enter GPU', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_10xlarge', models.CharField(help_text=b'Please enter Instance Capacity_10xlarge', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_2xlarge', models.CharField(help_text=b'Please enter Instance_Capacity_2xlarge', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_4xlarge', models.CharField(help_text=b'Please enter Instance_Capacity_4xlarge', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_8xlarge', models.CharField(help_text=b'Please enter Instance_Capacity_8xlarge', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_large', models.CharField(help_text=b'Please enter Instance_Capacity_large', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_medium', models.CharField(help_text=b'Please enter Instance_Capacity_medium', max_length=200, null=True, blank=True)),
                ('Instance_Capacity_xlarge', models.CharField(help_text=b'Please enter Instance_Capacity_xlarge', max_length=200, null=True, blank=True)),
                ('Intel_AVX_Available', models.CharField(help_text=b'Please enter Intel_AVX_Available', max_length=200, null=True, blank=True)),
                ('Intel_AVX2_Available', models.CharField(help_text=b'Please enter Intel_AVX2_Available', max_length=200, null=True, blank=True)),
                ('Intel_Turbo_Available', models.CharField(help_text=b'Please enter Intel_Turbo_Available', max_length=200, null=True, blank=True)),
                ('Physical_Cores', models.CharField(help_text=b'Please enter Physical_Cores', max_length=200, null=True, blank=True)),
                ('Pre_Installed_SW', models.CharField(help_text=b'Please enter Pre_Installed_SW', max_length=200, null=True, blank=True)),
                ('Processor_Features', models.CharField(help_text=b'Please enter Processor_Features', max_length=200, null=True, blank=True)),
                ('Sockets', models.CharField(help_text=b'Please enter Sockets', max_length=200, null=True, blank=True)),
                ('product_code', silver.utils.models.UnsavedForeignKey(help_text=b'The product code for this plan.', to='silver.ProductCode')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
