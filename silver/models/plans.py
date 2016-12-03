# Copyright (c) 2016 Presslabs SRL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from model_utils import Choices

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from silver.utils.international import currencies
from silver.utils.models import UnsavedForeignKey
from datetime import datetime


class Plan(models.Model):
    class INTERVALS(object):
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'
        YEAR = 'year'

    INTERVAL_CHOICES = Choices(
        (INTERVALS.DAY, _('Day')),
        (INTERVALS.WEEK, _('Week')),
        (INTERVALS.MONTH, _('Month')),
        (INTERVALS.YEAR, _('Year'))
    )

    name = models.CharField(
        max_length=200, help_text='Display name of the plan.',
        db_index=True
    )
    interval = models.CharField(
        choices=INTERVAL_CHOICES, max_length=12, default=INTERVALS.MONTH,
        help_text='The frequency with which a subscription should be billed.'
    )
    interval_count = models.PositiveIntegerField(
        help_text='The number of intervals between each subscription billing'
    )
    amount = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The amount in the specified currency to be charged on the '
                  'interval specified.',
    )
    currency = models.CharField(
        choices=currencies, max_length=4, default='USD',
        help_text='The currency in which the subscription will be charged.'
    )
    trial_period_days = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Number of trial period days granted when subscribing a '
                  'customer to this plan.',
        verbose_name='Trial days'
    )

    metered_features = models.ManyToManyField(
        'MeteredFeature', blank=True,default="No Value",
        help_text="A list of the plan's metered features."
    )

    rds_metered_feature = models.ManyToManyField(
        'RDS', blank=True,default="No Value",
        help_text="A list of the plan's RDS metered features."
    )


    s3_metered_features = models.ManyToManyField(
        'S3Storage', blank=True,default="No Value",
        help_text="A list of the plan's S3 metered features."
    )

    LoadBalencer_metered = models.ManyToManyField(
        'LoadBalencer', blank=True,default="No Value",
        help_text="A list of the plan's metered features."
    )

    instance_count=models.IntegerField(default=0)
    rds_count=models.IntegerField(default=0)
    s3_count=models.IntegerField(default=0)
    balancer_count=models.IntegerField(default=0)

    generate_after = models.PositiveIntegerField(
        default=0,
        help_text='Number of seconds to wait after current billing cycle ends '
                  'before generating the invoice. This can be used to allow '
                  'systems to finish updating feature counters.'
    )
    enabled = models.BooleanField(default=True,
                                  help_text='Whether to accept subscriptions.')
    private = models.BooleanField(default=False,
                                  help_text='Indicates if a plan is private.')
    product_code = models.ForeignKey(
        'ProductCode', help_text='The product code for this plan.'
    )
    provider = models.ForeignKey(
        'Provider', related_name='plans',
        help_text='The provider which provides the plan.'
    )

    instance_price= models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
       blank=True
    )
    rds_price= models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
       blank=True
    )
    s3_price= models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
       blank=True
    )
    balancer_price= models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
       blank=True
    )
    


    class Meta:
        ordering = ('name',)

    @staticmethod
    def validate_metered_features(metered_features):
        product_codes = dict()
        for mf in metered_features:
            if product_codes.get(mf.product_code.value, None):
                err_msg = 'A plan cannot have two or more metered features ' \
                          'with the same product code. (%s, %s)' \
                          % (mf.name, product_codes.get(mf.product_code.value))
                raise ValidationError(err_msg)
            product_codes[mf.product_code.value] = mf.name

    def __unicode__(self):
        return unicode(self.name)

    @property
    def provider_flow(self):
        return self.provider.flow

    def _get_amount(self):
        self.metered_features.aggregate(total=models.Sum('price_per_unit'))
        self.instance_count*self.metered_features.aggregate(total=models.Sum('price_per_unit'))['total']

        return (self.instance_count*self.metered_features.aggregate(total=models.Sum('price_per_unit'))['total'])
    product_count=property(_get_amount)

    def _get_instance_cost(self):
        instance_price=None
        instance_price=self.metered_features.aggregate(total=models.Sum('price_per_unit'))['total']
        if instance_price==None:
            instance_price=0

        return ((self.instance_count*instance_price)*24*30)

    def _get_rds_cost(self):
        rdsprice=None
        rdsprice=self.rds_metered_feature.aggregate(total=models.Sum('price_per_unit'))['total']

        if rdsprice==None:
            rdsprice=0

        return ((self.rds_count*rdsprice)*24*30)

    def _get_s3_cost(self):
        s3price=None
        s3price=self.s3_metered_features.aggregate(total=models.Sum('price_per_unit'))['total']
        if s3price==None:
            s3price=0
        '''S3 Cost given to Monthly'''
        return ((self.s3_count*s3price))

    def _get_loadbalancer_cost(self):
        balacer_price=None
        balacer_price=self.LoadBalencer_metered.aggregate(total=models.Sum('price_per_unit'))['total']
        if balacer_price==None:
            balacer_price=0

        return ((self.balancer_count*balacer_price)*24*30)

    
    def _get_total_plan_cost(self):
        
        balacer_price=None
        balacer_price=self.LoadBalencer_metered.aggregate(total=models.Sum('price_per_unit'))['total']
        if balacer_price==None:
            balacer_price=0
        
        s3price=None
        s3price=self.s3_metered_features.aggregate(total=models.Sum('price_per_unit'))['total']
        if s3price==None:
            s3price=0
        
        rdsprice=None
        rdsprice=self.rds_metered_feature.aggregate(total=models.Sum('price_per_unit'))['total']
        if rdsprice==None:
            rdsprice=0

        instance_price=None
        instance_price=self.metered_features.aggregate(total=models.Sum('price_per_unit'))['total']
        if instance_price==None:
            instance_price=0
        return (
            ((self.instance_count*instance_price)*24*30)+
            ((self.rds_count*rdsprice)*24*30)+
            (self.s3_count*s3price)+
            ((self.balancer_count*balacer_price))*24*30
            )


    def _get_instance_name(self):
        instance_name=self.metered_features.all().values_list('name')
        return instance_name

    def _get_rds_name(self):
        instance_name=self.rds_metered_feature.all().values_list('Instance_Type')
        return instance_name

    def _get_balancer_name(self):
        instance_name=self.LoadBalencer_metered.all().values_list('PriceDescription')
        return instance_name

    def _get_s3_name(self):
        instance_name=self.s3_metered_features.all().values_list('PriceDescription')
        return instance_name

    instance_cost=property( _get_instance_cost)
    rds_cost=property( _get_rds_cost)
    loadbalancer_cost=property( _get_loadbalancer_cost)
    s3_cost=property( _get_s3_cost)
    instance_name=property( _get_instance_name)
    rds_name=property(  _get_rds_name)
    balancer_name=property( _get_balancer_name)
    s3_name=property( _get_s3_name)
    total_plan_price=property(_get_total_plan_cost)



class Region(models.Model):
    region = models.CharField(
        max_length=200,
        help_text='Please enter Region name',
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Region"

    def __str__(self):
        return self.region

class MeteredFeature(models.Model):
    region = models.CharField(
        max_length=200,
        help_text='Please enter Region name',
        blank=True,
        null=True,
    )

    ostype = models.CharField(
        max_length=200,
        help_text='Please enter OS Type',
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=200,
        help_text='The feature display name.',
        db_index=True,
    )
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The price per unit.',
    )
    included_units = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The number of included units per plan interval.'
    )
    included_units_during_trial = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        blank=True, null=True,
        help_text='The number of included units during the trial period.'
    )


    EBS_volume = models.IntegerField(
        help_text='Please enter EBS Volume ',
        blank=True,
        null=True,

    )

    Elastic_IP= models.CharField(
        max_length=200,
        help_text='Please enter Elastic IP',
        blank=True,
        null=True,
    )

    termstype= models.CharField(
        max_length=200,
        help_text='Please enter Termstype',
        blank=True,
        null=True,
    )

    PriceDescription=models.TextField(blank=True,null=True)
    EffectiveDate=models.CharField(
        max_length=200,
        help_text='EffectiveDate',
        blank=True,
        null=True,
    )
    currency=models.CharField(
        max_length=200,
        help_text='Please enter currency',
        blank=True,
        null=True,
    )
    LeaseContractLength=models.CharField(
        max_length=200,
        help_text='Please enter LeaseContractLength',
        blank=True,
        null=True,
    )



    PurchaseOption=models.CharField(
        max_length=200,
        help_text='Please enter PurchaseOption',
        blank=True,
        null=True,
    )


    OfferingClass=models.CharField(
        max_length=200,
        help_text='Please enter OfferingClass',
        blank=True,
        null=True,
    )

    Product_Family= models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )

    serviceCode=models.CharField(
        max_length=200,
        help_text='Please enter serviceCode',
        blank=True,
        null=True,
    )

    Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter Location Type',
        blank=True,
        null=True,
    )



    Instance_Type=models.CharField(
        max_length=200,
        help_text='Please enter Instance Type',
        blank=True,
        null=True,
    )


    Current_Generation=models.CharField(
        max_length=200,
        help_text='Please enter Current Generation',
        blank=True,
        null=True,
    )
    Instance_Family=models.CharField(
        max_length=200,
        help_text='Please enter Instance Family',
        blank=True,
        null=True,
    )
    vCPU=models.CharField(
        max_length=200,
        help_text='Please enter vCPU',
        blank=True,
        null=True,
    )

    Physical_Processor=models.CharField(
        max_length=200,
        help_text='Please enter Physical Processor',
        blank=True,
        null=True,
    )
    Clock_Speed=models.CharField(
        max_length=200,
        help_text='Please enter Clock Speed',
        blank=True,
        null=True,
    )

    Memory=models.CharField(
        max_length=200,
        help_text='Please enter Memory',
        blank=True,
        null=True,
    )


    Storage=models.CharField(
        max_length=200,
        help_text='Please enter Storage',
        blank=True,
        null=True,
    )


    Network_Performance=models.CharField(
        max_length=200,
        help_text='Please enter Network Performance',
        blank=True,
        null=True,
    )
    Processor_Architecture=models.CharField(
        max_length=200,
        help_text='Please enter Processor Architecture',
        blank=True,
        null=True,
    )
    Storage_Media=models.CharField(
        max_length=200,
        help_text='Please enter Storage Media',
        blank=True,
        null=True,
    )

    Volume_Type=models.CharField(
        max_length=200,
        help_text='Please enter Volume Type',
        blank=True,
        null=True,
    )


    Max_Volume_Size=models.CharField(
        max_length=200,
        help_text='Please enter Max Volume Size',
        blank=True,
        null=True,
    )

    Max_IOPS_volume=models.CharField(
        max_length=200,
        help_text='Please enter Max IOPS_volume',
        blank=True,
        null=True,
    )

    Max_IOPS_Burst_Performance=models.CharField(
        max_length=200,
        help_text='Please enter Max_IOPS_Burst_Performance',
        blank=True,
        null=True,
    )

    Max_throughput_volume=models.CharField(
        max_length=200,
        help_text='Please enter Max_throughput_volume',
        blank=True,
        null=True,
    )
    Provisioned=models.CharField(
        max_length=200,
        help_text='Please enter Provisioned',
        blank=True,
        null=True,
    )

    Tenancy=models.CharField(
        max_length=200,
        help_text='Please enter Tenancy',
        blank=True,
        null=True,
    )


    EBS_Optimized=models.CharField(
        max_length=200,
        help_text='Please enter EBS_Optimize',
        blank=True,
        null=True,
    )


    Operating_System=models.CharField(
        max_length=200,
        help_text='Please enter Operating_System',
        blank=True,
        null=True,
    )
    License_Model=models.CharField(
        max_length=200,
        help_text='Please enter License_Model',
        blank=True,
        null=True,
    )

    Group=models.CharField(
        max_length=200,
        help_text='Please enter Group',
        blank=True,
        null=True,
    )

    Group_Description=models.CharField(
        max_length=200,
        help_text='Please enter Group_Description',
        blank=True,
        null=True,
    )


    Transfer_Type=models.CharField(
        max_length=200,
        help_text='Please enter Transfer_Type',
        blank=True,
        null=True,
    )
    From_Location=models.CharField(
        max_length=200,
        help_text='Please enter From_Location',
        blank=True,
        null=True,
    )
    From_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter From_Location_Type',
        blank=True,
        null=True,
    )

    To_Location=models.CharField(
        max_length=200,
        help_text='Please enter To_Location',
        blank=True,
        null=True,
    )

    To_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter To_Location_Type',
        blank=True,
        null=True,
    )

    usageType=models.CharField(
        max_length=200,
        help_text='Please enter usageType',
        blank=True,
        null=True,
    )

    operation=models.CharField(
        max_length=200,
        help_text='Please enter operation',
        blank=True,
        null=True,
    )
    Dedicated_EBS_Throughput=models.CharField(
        max_length=200,
        help_text='Please enter Dedicated_EBS_Throughput',
        blank=True,
        null=True,
    )



    Enhanced_Networking_Supported=models.CharField(
        max_length=200,
        help_text='Please enter Enhanced_Networking_Supported',
        blank=True,
        null=True,
    )
    GPU=models.CharField(
        max_length=200,
        help_text='Please enter GPU',
        blank=True,
        null=True,
    )
    Instance_Capacity_10xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance Capacity_10xlarge',
        blank=True,
        null=True,)

    Instance_Capacity_2xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_2xlarge',
        blank=True,
        null=True,)
    Instance_Capacity_4xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_4xlarge',
        blank=True,
        null=True,)
    Instance_Capacity_8xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_8xlarge',
        blank=True,
        null=True,)

    Instance_Capacity_large=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_large',
        blank=True,
        null=True,)

    Instance_Capacity_medium=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_medium',
        blank=True,
        null=True,)
    Instance_Capacity_xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_xlarge',
        blank=True,
        null=True,)
    Intel_AVX_Available=models.CharField(
        max_length=200,
        help_text='Please enter Intel_AVX_Available',
        blank=True,
        null=True,)

    Intel_AVX2_Available=models.CharField(
        max_length=200,
        help_text='Please enter Intel_AVX2_Available',
        blank=True,
        null=True,)

    Intel_Turbo_Available=models.CharField(
        max_length=200,
        help_text='Please enter Intel_Turbo_Available',
        blank=True,
        null=True,)
    Physical_Cores=models.CharField(
        max_length=200,
        help_text='Please enter Physical_Cores',
        blank=True,
        null=True,)
    Pre_Installed_SW=models.CharField(
        max_length=200,
        help_text='Please enter Pre_Installed_SW',
        blank=True,
        null=True,)

    Processor_Features=models.CharField(
        max_length=200,
        help_text='Please enter Processor_Features',
        blank=True,
        null=True,)

    Sockets=models.CharField(
        max_length=200,
        help_text='Please enter Sockets',
        blank=True,
        null=True,)

    product_code = UnsavedForeignKey(
        'ProductCode', help_text='The product code for this plan.'
    )

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        fmt = u'{name} ({ostype},{price_per_unit},{PriceDescription})'
        return fmt.format(name=self.name, price_per_unit=self.price_per_unit,
                          ostype=self.ostype,PriceDescription=self.PriceDescription)



class RDS(models.Model):
    termstype= models.CharField(
        max_length=200,
        help_text='Please enter Termstype',
        blank=True,
        null=True,
    )

    PriceDescription=models.TextField(blank=True,null=True,)

    EffectiveDate=models.CharField(
        max_length=200,
        help_text='EffectiveDate',
        blank=True,
        null=True,
    )
    unit = models.CharField(max_length=20,blank=True,)


    price_per_unit = models.DecimalField(
        max_digits=19, decimal_places=10, validators=[MinValueValidator(0.0)],
        help_text='The price per unit.',
    )


    currency=models.CharField(
        max_length=200,
        help_text='Please enter currency',
        blank=True,
        null=True,
    )


    LeaseContractLength=models.CharField(
        max_length=200,
        help_text='Please enter LeaseContractLength',
        blank=True,
        null=True,
    )


    PurchaseOption=models.CharField(
        max_length=200,
        help_text='Please enter PurchaseOption',
        blank=True,
        null=True,
    )



    OfferingClass=models.CharField(
        max_length=200,
        help_text='Please enter OfferingClass',
        blank=True,
        null=True,
    )

    Product_Family= models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )



    StartingRange=models.IntegerField(
        help_text='Please enter StartingRange ',
        blank=True,
        null=True,

    )


    EndingRange=models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )

    RelatedTo=models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )

    serviceCode=models.CharField(
        max_length=200,
        help_text='Please enter serviceCode',
        blank=True,
        null=True,
    )


    Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter Location Type',
        blank=True,
        null=True,
    )


    region = models.CharField(
        max_length=200,
        help_text='Please enter Region name',
        blank=True,
        null=True,
    )

    Instance_Type=models.CharField(
        max_length=200,
        help_text='Please enter Instance Type',
        blank=True,
        null=True,
    )

    Current_Generation=models.CharField(
        max_length=200,
        help_text='Please enter Current Generation',
        blank=True,
        null=True,
    )
    Instance_Family=models.CharField(
        max_length=200,
        help_text='Please enter Instance Family',
        blank=True,
        null=True,
    )

    vCPU=models.CharField(
        max_length=200,
        help_text='Please enter vCPU',
        blank=True,
        null=True,
    )


    Physical_Processor=models.CharField(
        max_length=200,
        help_text='Please enter Physical Processor',
        blank=True,
        null=True,
    )
    Clock_Speed=models.CharField(
        max_length=200,
        help_text='Please enter Clock Speed',
        blank=True,
        null=True,
    )

    Memory=models.CharField(
        max_length=200,
        help_text='Please enter Memory',
        blank=True,
        null=True,
    )

    Processor_Architecture=models.CharField(
        max_length=200,
        help_text='Please enter Processor Architecture',
        blank=True,
        null=True,
    )
    
    Storage=models.CharField(
        max_length=200,
        help_text='Please enter Storage',
        blank=True,
        null=True,
    )

    Network_Performance=models.CharField(
        max_length=200,
        help_text='Please enter Network Performance',
        blank=True,
        null=True,
    )

    engine_code=models.IntegerField(
        help_text='Please enter engine_code ',
        blank=True,
        null=True,

    )

    Database_Engine=models.CharField(
        max_length=200,
        help_text='Please enter  Database_Engine',
        blank=True,
        null=True,
    )
    Database_Edition=models.CharField(
        max_length=200,
        help_text='Please enter Database_Edition',
        blank=True,
        null=True,
    )
    License_Model=models.CharField(
        max_length=200,
        help_text='Please enter License_Model',
        blank=True,
        null=True,
    )

    Deployment_Option=models.CharField(
        max_length=200,
        help_text='Please enter Deployment_Option',
        blank=True,
        null=True,
    )

    Transfer_Type=models.CharField(
        max_length=200,
        help_text='Please enter Transfer_Type',
        blank=True,
        null=True,
    )

    From_Location=models.CharField(
        max_length=200,
        help_text='Please enter From_Location',
        blank=True,
        null=True,
    )
    From_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter From_Location_Type',
        blank=True,
        null=True,
    )

    To_Location=models.CharField(
        max_length=200,
        help_text='Please enter To_Location',
        blank=True,
        null=True,
    )

    To_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter To_Location_Type',
        blank=True,
        null=True,
    )

    usageType=models.CharField(
        max_length=200,
        help_text='Please enter usageType',
        blank=True,
        null=True,
    )

    operation=models.CharField(
        max_length=200,
        help_text='Please enter operation',
        blank=True,
        null=True,
    )
    Dedicated_EBS_Throughput=models.CharField(
        max_length=200,
        help_text='Please enter Dedicated_EBS_Throughput',
        blank=True,
        null=True,
    )

    Enhanced_Networking_Supported=models.CharField(
        max_length=500,
        help_text='Please enter Enhanced_Networking_Supported',
        blank=True,
        null=True,
    )

    Processor_Features=models.CharField(
        max_length=200,
        help_text='Please enter Processor_Features',
        blank=True,
        null=True,)

    def __unicode__(self):
        fmt = u'{Instance_Type} ({Database_Engine},{price_per_unit},{PriceDescription})'
        return fmt.format(Instance_Type=self.Instance_Type, price_per_unit=self.price_per_unit,
                          Database_Engine=self.Database_Engine,PriceDescription=self.PriceDescription)



class S3Storage(models.Model):
    SKU=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)    
    OfferTermCode=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)
    RateCode=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)
    termstype=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)
    PriceDescription=models.TextField(blank=True,null=True)
    EffectiveDate=models.CharField(
        max_length=200,
        help_text='EffectiveDate',
        blank=True,
        null=True,
    )

    StartingRange=models.IntegerField(
        help_text='Please enter StartingRange ',
        blank=True,
        null=True,
    )
    EndingRange=models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )
    
    Unit=models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )
    price_per_unit=models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The price per unit.',
    )
    currency = models.CharField(
        choices=currencies, max_length=4, default='USD',
        help_text='The currency in which the subscription will be charged.'
    )

    RelatedTo=models.CharField(
        max_length=200,
        help_text='Please enter RelatedTo',
        blank=True,
        null=True,
    )


    Product_Family= models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )
    serviceCode=models.CharField(
        max_length=200,
        help_text='Please enter serviceCode',
        blank=True,
        null=True,
    )
    


    region=models.CharField(
        max_length=200,
        help_text='Please enter region',
        blank=True,
        null=True,
    )
    Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter Location Type',
        blank=True,
        null=True,
    )
    Availability=models.CharField(
        max_length=200,
        help_text='Availability',
        blank=True,
        null=True,
    )
    Storage_class=models.CharField(
        max_length=200,
        help_text='Please enter Storage Class',
        blank=True,
        null=True,
    )
    Volume_Type=models.CharField(
        max_length=200,
        help_text='Please enter Volume Type',
        blank=True,
        null=True,
    )
    Fee_Code=models.CharField(
        max_length=200,
        help_text='Please enter Volume Type',
        blank=True,
        null=True,
    )
    Fee_Description=models.CharField(
        max_length=200,
        help_text='Please enter Volume Type',
        blank=True,
        null=True,
    )
    Group=models.CharField(
        max_length=200,
        help_text='Please enter Group',
        blank=True,
        null=True,
    )
    Group_Description=models.CharField(
        max_length=200,
        help_text='Please enter Group_Description',
        blank=True,
        null=True,
    )
    Transfer_Type=models.CharField(
        max_length=200,
        help_text='Please enter Transfer_Type',
        blank=True,
        null=True,
    )
    From_Location=models.CharField(
        max_length=200,
        help_text='Please enter From_Location',
        blank=True,
        null=True,
    )
    From_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter From_Location_Type',
        blank=True,
        null=True,
    )

    To_Location=models.CharField(
        max_length=200,
        help_text='Please enter To_Location',
        blank=True,
        null=True,
    )

    To_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter To_Location_Type',
        blank=True,
        null=True,
    )

    usageType=models.CharField(
        max_length=200,
        help_text='Please enter usageType',
        blank=True,
        null=True,
    )

    operation=models.CharField(
        max_length=200,
        help_text='Please enter operation',
        blank=True,
        null=True,
    )
    Durability=models.CharField(
        max_length=200,
        help_text='Durability',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        fmt = u'{PriceDescription}'
        return fmt.format(PriceDescription=self.PriceDescription)

class SES_Storage(models.Model):
    SKU=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)    
    OfferTermCode=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)
    RateCode=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)
    termstype=models.CharField(
        max_length=200,
        help_text='Please enter SKU',
        blank=True,
        null=True,)
    PriceDescription=models.TextField(blank=True,null=True)
    EffectiveDate=models.CharField(
        max_length=200,
        help_text='EffectiveDate',
        blank=True,
        null=True,
    )

    StartingRange=models.IntegerField(
        help_text='Please enter StartingRange ',
        blank=True,
        null=True,
    )
    EndingRange=models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )
    
    Unit=models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )
    price_per_unit=models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The price per unit.',
    )
    currency = models.CharField(
        choices=currencies, max_length=4, default='USD',
        help_text='The currency in which the subscription will be charged.'
    )
    Product_Family= models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )
    serviceCode=models.CharField(
        max_length=200,
        help_text='Please enter serviceCode',
        blank=True,
        null=True,
    )
    Description=models.TextField(blank=True,null=True)
    region=models.CharField(
        max_length=200,
        help_text='Please enter region',
        blank=True,
        null=True,
    )
    Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter Location Type',
        blank=True,
        null=True,
    )

    Origin=models.CharField(
        max_length=200,
        help_text='Origin',
        blank=True,
        null=True,
    )
    Group=models.CharField(
        max_length=200,
        help_text='Please enter Group',
        blank=True,
        null=True,
    )
    Group_Description=models.CharField(
        max_length=200,
        help_text='Please enter Group_Description',
        blank=True,
        null=True,
    )

    Transfer_Type=models.CharField(
        max_length=200,
        help_text='Please enter Transfer_Type',
        blank=True,
        null=True,
    )

    From_Location=models.CharField(
        max_length=200,
        help_text='Please enter From_Location',
        blank=True,
        null=True,
    )
    From_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter From_Location_Type',
        blank=True,
        null=True,
    )

    To_Location=models.CharField(
        max_length=200,
        help_text='Please enter To_Location',
        blank=True,
        null=True,
    )

    To_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter To_Location_Type',
        blank=True,
        null=True,
    )

    usageType=models.CharField(
        max_length=200,
        help_text='Please enter usageType',
        blank=True,
        null=True,
    )

    operation=models.CharField(
        max_length=200,
        help_text='Please enter operation',
        blank=True,
        null=True,
    )



    ContentType=models.CharField(
        max_length=200,
        help_text='Please enter From_Location',
        blank=True,
        null=True,
    )
    Recipient=models.CharField(
        max_length=200,
        help_text='Please enter From_Location_Type',
        blank=True,
        null=True,
    )


    def __unicode__(self):
        fmt = u'{PriceDescription}'
        return fmt.format(PriceDescription=self.PriceDescription)





class LoadBalencer(models.Model):
    region = models.CharField(
        max_length=200,
        help_text='Please enter Region name',
        blank=True,
        null=True,
    )

    ostype = models.CharField(
        max_length=200,
        help_text='Please enter OS Type',
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=200,
        help_text='The feature display name.',
        db_index=True,
    )
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The price per unit.',
    )
    included_units = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        help_text='The number of included units per plan interval.'
    )
    included_units_during_trial = models.DecimalField(
        max_digits=19, decimal_places=4, validators=[MinValueValidator(0.0)],
        blank=True, null=True,
        help_text='The number of included units during the trial period.'
    )


    EBS_volume = models.IntegerField(
        help_text='Please enter EBS Volume ',
        blank=True,
        null=True,

    )

    Elastic_IP= models.CharField(
        max_length=200,
        help_text='Please enter Elastic IP',
        blank=True,
        null=True,
    )

    termstype= models.CharField(
        max_length=200,
        help_text='Please enter Termstype',
        blank=True,
        null=True,
    )

    PriceDescription=models.TextField(blank=True,null=True)
    EffectiveDate=models.CharField(
        max_length=200,
        help_text='EffectiveDate',
        blank=True,
        null=True,
    )
    currency=models.CharField(
        max_length=200,
        help_text='Please enter currency',
        blank=True,
        null=True,
    )
    LeaseContractLength=models.CharField(
        max_length=200,
        help_text='Please enter LeaseContractLength',
        blank=True,
        null=True,
    )



    PurchaseOption=models.CharField(
        max_length=200,
        help_text='Please enter PurchaseOption',
        blank=True,
        null=True,
    )


    OfferingClass=models.CharField(
        max_length=200,
        help_text='Please enter OfferingClass',
        blank=True,
        null=True,
    )

    Product_Family= models.CharField(
        max_length=200,
        help_text='Please enter Product Family',
        blank=True,
        null=True,
    )

    serviceCode=models.CharField(
        max_length=200,
        help_text='Please enter serviceCode',
        blank=True,
        null=True,
    )

    Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter Location Type',
        blank=True,
        null=True,
    )



    Instance_Type=models.CharField(
        max_length=200,
        help_text='Please enter Instance Type',
        blank=True,
        null=True,
    )


    Current_Generation=models.CharField(
        max_length=200,
        help_text='Please enter Current Generation',
        blank=True,
        null=True,
    )
    Instance_Family=models.CharField(
        max_length=200,
        help_text='Please enter Instance Family',
        blank=True,
        null=True,
    )
    vCPU=models.CharField(
        max_length=200,
        help_text='Please enter vCPU',
        blank=True,
        null=True,
    )

    Physical_Processor=models.CharField(
        max_length=200,
        help_text='Please enter Physical Processor',
        blank=True,
        null=True,
    )
    Clock_Speed=models.CharField(
        max_length=200,
        help_text='Please enter Clock Speed',
        blank=True,
        null=True,
    )

    Memory=models.CharField(
        max_length=200,
        help_text='Please enter Memory',
        blank=True,
        null=True,
    )


    Storage=models.CharField(
        max_length=200,
        help_text='Please enter Storage',
        blank=True,
        null=True,
    )


    Network_Performance=models.CharField(
        max_length=200,
        help_text='Please enter Network Performance',
        blank=True,
        null=True,
    )
    Processor_Architecture=models.CharField(
        max_length=200,
        help_text='Please enter Processor Architecture',
        blank=True,
        null=True,
    )
    Storage_Media=models.CharField(
        max_length=200,
        help_text='Please enter Storage Media',
        blank=True,
        null=True,
    )

    Volume_Type=models.CharField(
        max_length=200,
        help_text='Please enter Volume Type',
        blank=True,
        null=True,
    )


    Max_Volume_Size=models.CharField(
        max_length=200,
        help_text='Please enter Max Volume Size',
        blank=True,
        null=True,
    )

    Max_IOPS_volume=models.CharField(
        max_length=200,
        help_text='Please enter Max IOPS_volume',
        blank=True,
        null=True,
    )

    Max_IOPS_Burst_Performance=models.CharField(
        max_length=200,
        help_text='Please enter Max_IOPS_Burst_Performance',
        blank=True,
        null=True,
    )

    Max_throughput_volume=models.CharField(
        max_length=200,
        help_text='Please enter Max_throughput_volume',
        blank=True,
        null=True,
    )
    Provisioned=models.CharField(
        max_length=200,
        help_text='Please enter Provisioned',
        blank=True,
        null=True,
    )

    Tenancy=models.CharField(
        max_length=200,
        help_text='Please enter Tenancy',
        blank=True,
        null=True,
    )


    EBS_Optimized=models.CharField(
        max_length=200,
        help_text='Please enter EBS_Optimize',
        blank=True,
        null=True,
    )


    Operating_System=models.CharField(
        max_length=200,
        help_text='Please enter Operating_System',
        blank=True,
        null=True,
    )
    License_Model=models.CharField(
        max_length=200,
        help_text='Please enter License_Model',
        blank=True,
        null=True,
    )

    Group=models.CharField(
        max_length=200,
        help_text='Please enter Group',
        blank=True,
        null=True,
    )

    Group_Description=models.CharField(
        max_length=200,
        help_text='Please enter Group_Description',
        blank=True,
        null=True,
    )


    Transfer_Type=models.CharField(
        max_length=200,
        help_text='Please enter Transfer_Type',
        blank=True,
        null=True,
    )
    From_Location=models.CharField(
        max_length=200,
        help_text='Please enter From_Location',
        blank=True,
        null=True,
    )
    From_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter From_Location_Type',
        blank=True,
        null=True,
    )

    To_Location=models.CharField(
        max_length=200,
        help_text='Please enter To_Location',
        blank=True,
        null=True,
    )

    To_Location_Type=models.CharField(
        max_length=200,
        help_text='Please enter To_Location_Type',
        blank=True,
        null=True,
    )

    usageType=models.CharField(
        max_length=200,
        help_text='Please enter usageType',
        blank=True,
        null=True,
    )

    operation=models.CharField(
        max_length=200,
        help_text='Please enter operation',
        blank=True,
        null=True,
    )
    Dedicated_EBS_Throughput=models.CharField(
        max_length=200,
        help_text='Please enter Dedicated_EBS_Throughput',
        blank=True,
        null=True,
    )



    Enhanced_Networking_Supported=models.CharField(
        max_length=200,
        help_text='Please enter Enhanced_Networking_Supported',
        blank=True,
        null=True,
    )
    GPU=models.CharField(
        max_length=200,
        help_text='Please enter GPU',
        blank=True,
        null=True,
    )
    Instance_Capacity_10xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance Capacity_10xlarge',
        blank=True,
        null=True,)

    Instance_Capacity_2xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_2xlarge',
        blank=True,
        null=True,)
    Instance_Capacity_4xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_4xlarge',
        blank=True,
        null=True,)
    Instance_Capacity_8xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_8xlarge',
        blank=True,
        null=True,)

    Instance_Capacity_large=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_large',
        blank=True,
        null=True,)

    Instance_Capacity_medium=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_medium',
        blank=True,
        null=True,)
    Instance_Capacity_xlarge=models.CharField(
        max_length=200,
        help_text='Please enter Instance_Capacity_xlarge',
        blank=True,
        null=True,)
    Intel_AVX_Available=models.CharField(
        max_length=200,
        help_text='Please enter Intel_AVX_Available',
        blank=True,
        null=True,)

    Intel_AVX2_Available=models.CharField(
        max_length=200,
        help_text='Please enter Intel_AVX2_Available',
        blank=True,
        null=True,)

    Intel_Turbo_Available=models.CharField(
        max_length=200,
        help_text='Please enter Intel_Turbo_Available',
        blank=True,
        null=True,)
    Physical_Cores=models.CharField(
        max_length=200,
        help_text='Please enter Physical_Cores',
        blank=True,
        null=True,)
    Pre_Installed_SW=models.CharField(
        max_length=200,
        help_text='Please enter Pre_Installed_SW',
        blank=True,
        null=True,)

    Processor_Features=models.CharField(
        max_length=200,
        help_text='Please enter Processor_Features',
        blank=True,
        null=True,)

    Sockets=models.CharField(
        max_length=200,
        help_text='Please enter Sockets',
        blank=True,
        null=True,)

    product_code = models.ForeignKey(
        'ProductCode', help_text='The product code for this plan.'
    )
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        fmt = u'({ostype},{price_per_unit},{PriceDescription})'
        return fmt.format(price_per_unit=self.price_per_unit,
                          ostype=self.ostype,PriceDescription=self.PriceDescription)
