# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0015_auto_20161102_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteredfeature',
            name='Clock_Speed',
            field=models.CharField(help_text=b'Please enter Clock Speed', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Current_Generation',
            field=models.CharField(help_text=b'Please enter Current Generation', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Dedicated_EBS_Throughput',
            field=models.CharField(help_text=b'Please enter Dedicated_EBS_Throughput', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='EBS_Optimized',
            field=models.CharField(help_text=b'Please enter EBS_Optimize', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='EffectiveDate',
            field=models.DateTimeField(default=b'2016-11-04 05:04:53.622950', blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Enhanced_Networking_Supported',
            field=models.CharField(help_text=b'Please enter Enhanced_Networking_Supported', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='From_Location',
            field=models.CharField(help_text=b'Please enter From_Location', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='From_Location_Type',
            field=models.CharField(help_text=b'Please enter From_Location_Type', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='GPU',
            field=models.CharField(help_text=b'Please enter GPU', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Group',
            field=models.CharField(help_text=b'Please enter Group', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Group_Description',
            field=models.CharField(help_text=b'Please enter Group_Description', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_10xlarge',
            field=models.CharField(help_text=b'Please enter Instance Capacity_10xlarge', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_2xlarge',
            field=models.CharField(help_text=b'Please enter Instance_Capacity_2xlarge', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_4xlarge',
            field=models.CharField(help_text=b'Please enter Instance_Capacity_4xlarge', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_8xlarge',
            field=models.CharField(help_text=b'Please enter Instance_Capacity_8xlarge', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_large',
            field=models.CharField(help_text=b'Please enter Instance_Capacity_large', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_medium',
            field=models.CharField(help_text=b'Please enter Instance_Capacity_medium', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Capacity_xlarge',
            field=models.CharField(help_text=b'Please enter Instance_Capacity_xlarge', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Family',
            field=models.CharField(help_text=b'Please enter Instance Family', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Instance_Type',
            field=models.CharField(help_text=b'Please enter Instance Type', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Intel_AVX2_Available',
            field=models.CharField(help_text=b'Please enter Intel_AVX2_Available', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Intel_AVX_Available',
            field=models.CharField(help_text=b'Please enter Intel_AVX_Available', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Intel_Turbo_Available',
            field=models.CharField(help_text=b'Please enter Intel_Turbo_Available', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='LeaseContractLength',
            field=models.CharField(help_text=b'Please enter LeaseContractLength', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='License_Model',
            field=models.CharField(help_text=b'Please enter License_Model', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Location_Type',
            field=models.CharField(help_text=b'Please enter Location Type', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Max_IOPS_Burst_Performance',
            field=models.CharField(help_text=b'Please enter Max_IOPS_Burst_Performance', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Max_IOPS_volume',
            field=models.CharField(help_text=b'Please enter Max IOPS_volume', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Max_Volume_Size',
            field=models.CharField(help_text=b'Please enter Max Volume Size', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Max_throughput_volume',
            field=models.CharField(help_text=b'Please enter Max_throughput_volume', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Memory',
            field=models.CharField(help_text=b'Please enter Memory', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Network_Performance',
            field=models.CharField(help_text=b'Please enter Network Performance', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='OfferingClass',
            field=models.CharField(help_text=b'Please enter OfferingClass', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Operating_System',
            field=models.CharField(help_text=b'Please enter Operating_System', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Physical_Cores',
            field=models.CharField(help_text=b'Please enter Physical_Cores', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Physical_Processor',
            field=models.CharField(help_text=b'Please enter Physical Processor', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Pre_Installed_SW',
            field=models.CharField(help_text=b'Please enter Pre_Installed_SW', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='PriceDescription',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Processor_Architecture',
            field=models.CharField(help_text=b'Please enter Processor Architecture', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Processor_Features',
            field=models.CharField(help_text=b'Please enter Processor_Features', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Product_Family',
            field=models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Provisioned',
            field=models.CharField(help_text=b'Please enter Provisioned', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='PurchaseOption',
            field=models.CharField(help_text=b'Please enter PurchaseOption', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Sockets',
            field=models.CharField(help_text=b'Please enter Sockets', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Storage',
            field=models.CharField(help_text=b'Please enter Storage', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Storage_Media',
            field=models.CharField(help_text=b'Please enter Storage Media', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Tenancy',
            field=models.CharField(help_text=b'Please enter Tenancy', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='To_Location',
            field=models.CharField(help_text=b'Please enter To_Location', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='To_Location_Type',
            field=models.CharField(help_text=b'Please enter To_Location_Type', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Transfer_Type',
            field=models.CharField(help_text=b'Please enter Transfer_Type', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='Volume_Type',
            field=models.CharField(help_text=b'Please enter Volume Type', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='currency',
            field=models.CharField(help_text=b'Please enter currency', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='operation',
            field=models.CharField(help_text=b'Please enter operation', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='serviceCode',
            field=models.CharField(help_text=b'Please enter serviceCode', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='termstype',
            field=models.CharField(help_text=b'Please enter Termstype', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='usageType',
            field=models.CharField(help_text=b'Please enter usageType', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meteredfeature',
            name='vCPU',
            field=models.CharField(help_text=b'Please enter vCPU', max_length=200, null=True, blank=True),
        ),
    ]
