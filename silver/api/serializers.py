# Copyright (c) 2015 Presslabs SRL
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


from django_fsm import TransitionNotAllowed
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError as APIValidationError

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from silver.models import (MeteredFeatureUnitsLog, Customer, Subscription,
                           MeteredFeature, Plan, Provider, Invoice,
                           DocumentEntry, ProductCode, Proforma, Payment)
from silver.models.billing_entities.base import UserArchitectures
from silver.models.product_codes import ProductCode,Billing_ArchitectureType,Billing_Architecture,Billing_FeatureArchitecture
from silver.models.plans import Region,RDS,S3Storage,LoadBalencer

class ProductCodeRelatedField(serializers.SlugRelatedField):
    def __init__(self, **kwargs):
        super(ProductCodeRelatedField, self).__init__(
            slug_field='value', queryset=ProductCode.objects.all(), **kwargs)

    def to_internal_value(self, data):
        try:
            return ProductCode.objects.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return ProductCode(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

class ArchitectureRelatedField(serializers.SlugRelatedField):
    def __init__(self, **kwargs):
        super(ArchitectureRelatedField, self).__init__(
            slug_field='id', queryset=Billing_Architecture.objects.all(), **kwargs)

    def to_internal_value(self, data):
        try:
            return Billing_Architecture.objects.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return Billing_Architecture(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')





class MeteredFeatureSerializer(serializers.ModelSerializer):
    product_code = ProductCodeRelatedField()

    class Meta:
        model = MeteredFeature
        # fields = ('region','ostype','name', 'unit', 'price_per_unit', 'included_units',
        #           'product_code','EBS_volume','Elastic_IP','termstype','PriceDescription','EffectiveDate','currency','LeaseContractLength','PurchaseOption','OfferingClass',
        #           'Product_Family','serviceCode','Location_Type','Instance_Type','Current_Generation','Instance_Family','vCPU',
        #           'Physical_Processor','Clock_Speed','Memory','Storage','Network_Performance','Processor_Architecture','Storage_Media',
        #           'Volume_Type','Max_Volume_Size','Max_IOPS_volume','Max_IOPS_Burst_Performance','Max_throughput_volume','Provisioned','Tenancy','EBS_Optimized','Operating_System','License_Model','Group',
        #           'Group_Description','Transfer_Type','From_Location','From_Location_Type','To_Location','To_Location_Type',
        #           'usageType','operation','Dedicated_EBS_Throughput','Enhanced_Networking_Supported','GPU','Instance_Capacity_10xlarge','Instance_Capacity_2xlarge','Instance_Capacity_4xlarge','Instance_Capacity_8xlarge',
        #           'Instance_Capacity_large','Instance_Capacity_medium','Instance_Capacity_xlarge','Intel_AVX_Available','Intel_AVX2_Available','Intel_Turbo_Available','Physical_Cores','Pre_Installed_SW','Processor_Features','Sockets')
        
        fields = ('price_per_unit',
                  'product_code',)



    def create(self, validated_data):
        product_code = validated_data.pop('product_code')
        product_code.save()

        validated_data.update({'product_code': product_code})

        metered_feature = MeteredFeature.objects.create(**validated_data)

        return metered_feature


class MFUnitsLogUrl(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        customer_pk = request.parser_context['kwargs']['customer_pk']
        subscription_pk = request.parser_context['kwargs']['subscription_pk']
        kwargs = {
            'customer_pk': customer_pk,
            'subscription_pk': subscription_pk,
            'mf_product_code': obj.product_code.value
        }
        return self.reverse(view_name, kwargs=kwargs, request=request,
                            format=format)


class MeteredFeatureInSubscriptionSerializer(MeteredFeatureSerializer):
    url = MFUnitsLogUrl(view_name='mf-log-units', source='*', read_only=True)

    class Meta(MeteredFeatureSerializer.Meta):
        fields = MeteredFeatureSerializer.Meta.fields + ('url', )


class MFUnitsLogSerializer(serializers.HyperlinkedModelSerializer):
    # The 2 lines below are needed because of a DRF3 bug
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = MeteredFeatureUnitsLog
        fields = ('consumed_units', 'start_date', 'end_date')


class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        if not data:
            return data

        if (data is not None and not isinstance(data, dict) and
                not isinstance(data, list)):
                    raise ValidationError("Invalid JSON <{}>".format(data))
        return data

    def to_representation(self, value):
        return value


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    meta = JSONSerializerField(required=False)

    class Meta:
        model = Provider
        fields = ('id', 'url', 'name', 'company', 'invoice_series', 'flow',
                  'display_email', 'notification_email', 'address_1', 'address_2',
                  'city', 'state', 'zip_code', 'country', 'extra',
                  'invoice_series', 'invoice_starting_number',
                  'proforma_series', 'proforma_starting_number', 'meta')

    def validate(self, data):
        flow = data.get('flow', None)
        if flow == Provider.FLOWS.PROFORMA:
            if not data.get('proforma_starting_number', None) and\
               not data.get('proforma_series', None):
                errors = {'proforma_series': "This field is required as the "
                                             "chosen flow is proforma.",
                          'proforma_starting_number': "This field is required "
                                                      "as the chosen flow is "
                                                      "proforma."}
                raise serializers.ValidationError(errors)
            elif not data.get('proforma_series'):
                errors = {'proforma_series': "This field is required as the "
                                             "chosen flow is proforma."}
                raise serializers.ValidationError(errors)
            elif not data.get('proforma_starting_number', None):
                errors = {'proforma_starting_number': "This field is required "
                                                      "as the chosen flow is "
                                                      "proforma."}
                raise serializers.ValidationError(errors)

        return data


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    metered_features = MeteredFeatureSerializer(
        required=False, many=True
    )
    provider = serializers.HyperlinkedRelatedField(
        queryset=Provider.objects.all(),
        view_name='provider-detail',
    )
    product_code = ProductCodeRelatedField()

    class Meta:
        model = Plan
        fields = ('id','name', 'url', 'interval', 'interval_count', 'amount',
                  'currency', 'trial_period_days', 'generate_after', 'enabled',
                  'private', 'product_code', 'metered_features', 'provider','total_plan_price',
                  'instance_count','rds_count','s3_count','balancer_count')


    def validate_metered_features(self, value):
        metered_features = []
        for mf_data in value:
            metered_features.append(MeteredFeature(**mf_data))

        try:
            Plan.validate_metered_features(metered_features)
        except ValidationError, e:
            raise serializers.ValidationError(str(e)[3:-2])

        return value

    def create(self, validated_data):
        metered_features_data = validated_data.pop('metered_features')
        metered_features = []
        for mf_data in metered_features_data:
            mf = MeteredFeatureSerializer(data=mf_data)
            mf.is_valid(raise_exception=True)
            mf = mf.create(mf.validated_data)
            metered_features.append(mf)

        product_code = validated_data.pop('product_code')
        product_code.save()

        validated_data.update({'product_code': product_code})

        plan = Plan.objects.create(**validated_data)
        plan.metered_features.add(*metered_features)
        plan.product_code = product_code

        plan.save()

        return plan

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.generate_after = validated_data.get('generate_after',
                                                     instance.generate_after)
        instance.due_days = validated_data.get('due_days', instance.due_days)
        instance.save()

        return instance

class SubscriptionUrl(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'customer_pk': obj.customer.pk, 'subscription_pk': obj.pk}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    trial_end = serializers.DateField(required=False)
    start_date = serializers.DateField(required=False)
    ended_at = serializers.DateField(read_only=True)
    url = SubscriptionUrl(view_name='subscription-detail', source='*',
                          queryset=Subscription.objects.all(), required=False)
    updateable_buckets = serializers.ReadOnlyField()
    meta = JSONSerializerField(required=False)

    class Meta:
        model = Subscription
        fields = ('id', 'url', 'plan', 'customer', 'trial_end', 'start_date',
                  'ended_at', 'state', 'reference', 'updateable_buckets',
                  'meta', 'description')
        read_only_fields = ('state', 'updateable_buckets')

    def validate(self, attrs):
        instance = Subscription(**attrs)
        instance.clean()
        return attrs


class SubscriptionDetailSerializer(SubscriptionSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta(SubscriptionSerializer.Meta):
        fields = SubscriptionSerializer.Meta.fields + ('plan', )


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    subscriptions = SubscriptionUrl(view_name='subscription-detail', many=True,
                                    read_only=True)
    payments = serializers.HyperlinkedIdentityField(
        view_name='payment-list', source='*', lookup_url_kwarg='customer_pk'
    )
    meta = JSONSerializerField(required=False)

    class Meta:
        model = Customer
        fields = ('id', 'url', 'customer_reference', 'name', 'company',
                  'emails', 'address_1', 'address_2', 'city', 'state',
                  'zip_code', 'country', 'extra', 'sales_tax_number',
                  'sales_tax_name', 'sales_tax_percent', 'consolidated_billing',
                  'subscriptions', 'payments', 'meta','profile_img')





class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = ('id', 'value')


class DocumentEntrySerializer(serializers.HyperlinkedModelSerializer):
    product_code = serializers.SlugRelatedField(
        slug_field='value',
        read_only=True
    )

    class Meta:
        model = DocumentEntry
        fields = ('description', 'unit', 'unit_price', 'quantity', 'total',
                  'total_before_tax', 'start_date', 'end_date', 'prorated',
                  'product_code')


class PDFUrl(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        return request.build_absolute_uri(obj.pdf.url) if obj.pdf else None


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    invoice_entries = DocumentEntrySerializer(many=True)
    pdf_url = PDFUrl(view_name='', source='*', read_only=True)

    class Meta:
        model = Invoice
        fields = ('id', 'series', 'number', 'provider', 'customer',
                  'archived_provider', 'archived_customer', 'due_date',
                  'issue_date', 'paid_date', 'cancel_date', 'sales_tax_name',
                  'sales_tax_percent', 'currency', 'state', 'proforma',
                  'invoice_entries', 'total', 'pdf_url')
        read_only_fields = ('archived_provider', 'archived_customer', 'total')

    def create(self, validated_data):
        entries = validated_data.pop('invoice_entries', None)

        # Create the new invoice objectj
        invoice = Invoice.objects.create(**validated_data)

        # Add the invoice entries
        for entry in entries:
            entry_dict = dict()
            entry_dict['invoice'] = invoice
            for field in entry.items():
                entry_dict[field[0]] = field[1]

            DocumentEntry.objects.create(**entry_dict)

        return invoice

    def update(self, instance, validated_data):
        # The provider has changed => force the generation of the correct number
        # corresponding to the count of the new provider
        current_provider = instance.provider
        new_provider = validated_data.get('provider')
        if new_provider and new_provider != current_provider:
            instance.number = None

        updateable_fields = instance.updateable_fields
        for field_name in updateable_fields:
            field_value = validated_data.get(field_name,
                                             getattr(instance, field_name))
            setattr(instance, field_name, field_value)
        instance.save()

        return instance

    def validate(self, data):
        if self.instance:
            self.instance.clean()

        if self.instance and data['state'] != self.instance.state:
            msg = "Direct state modification is not allowed."\
                  " Use the corresponding endpoint to update the state."
            raise serializers.ValidationError(msg)
        return data


class ProformaSerializer(serializers.HyperlinkedModelSerializer):
    proforma_entries = DocumentEntrySerializer(many=True)
    pdf_url = PDFUrl(view_name='', source='*', read_only=True)

    class Meta:
        model = Proforma
        fields = ('id', 'series', 'number', 'provider', 'customer',
                  'archived_provider', 'archived_customer', 'due_date',
                  'issue_date', 'paid_date', 'cancel_date', 'sales_tax_name',
                  'sales_tax_percent', 'currency', 'state', 'invoice',
                  'proforma_entries', 'total', 'pdf_url')
        read_only_fields = ('archived_provider', 'archived_customer', 'total')

    def create(self, validated_data):
        entries = validated_data.pop('proforma_entries', None)

        proforma = Proforma.objects.create(**validated_data)

        for entry in entries:
            entry_dict = dict()
            entry_dict['proforma'] = proforma
            for field in entry.items():
                entry_dict[field[0]] = field[1]

            DocumentEntry.objects.create(**entry_dict)

        return proforma

    def update(self, instance, validated_data):
        # The provider has changed => force the generation of the correct number
        # corresponding to the count of the new provider
        current_provider = instance.provider
        new_provider = validated_data.get('provider')
        if new_provider and new_provider != current_provider:
            instance.number = None

        updateable_fields = instance.updateable_fields
        for field_name in updateable_fields:
            field_value = validated_data.get(field_name,
                                             getattr(instance, field_name))
            setattr(instance, field_name, field_value)
        instance.save()

        return instance

    def validate(self, data):
        if self.instance:
            self.instance.clean()

        if self.instance and data['state'] != self.instance.state:
            msg = "Direct state modification is not allowed."\
                  " Use the corresponding endpoint to update the state."
            raise serializers.ValidationError(msg)
        return data


class PaymentUrl(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'customer_pk': obj.customer.pk, 'payment_pk': obj.pk}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        return self.queryset.get(pk=view_kwargs['payment_pk'])


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    url = PaymentUrl(view_name='payment-detail', source='*',
                     read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'url', 'customer', 'provider', 'amount', 'currency',
                  'due_date', 'status', 'visible', 'proforma', 'invoice')

    def validate(self, attrs):
        if self.instance and self.instance.status in Payment.Status.FinalStatuses:
            message = "Cannot update a payment with '{}' status.".format(
                self.instance.status
            )
            raise serializers.ValidationError(message)

        # Run model clean and handle ValidationErrors
        try:
            # Use the existing instance to avoid unique field errors
            if self.instance:
                payment = self.instance
                payment_dict = payment.__dict__.copy()

                for attribute, value in attrs.items():
                    setattr(payment, attribute, value)

                payment.full_clean()

                # Revert changes to existing instance
                payment.__dict__ = payment_dict
            else:
                payment = Payment(**attrs)
                payment.full_clean()

        except ValidationError as e:
            errors = e.error_dict
            non_field_errors = errors.pop('__all__', None)
            if non_field_errors:
                errors['non_field_errors'] = [
                    error for sublist in non_field_errors for error in sublist
                ]

            raise serializers.ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        status = validated_data.pop('status', None)

        if status != instance.status:
            try:
                if status == Payment.Status.Paid:
                    instance.succeed()
                elif status == Payment.Status.Unpaid:
                    instance.fail()
                elif status == Payment.Status.Pending:
                    instance.process()
                elif status == Payment.Status.Canceled:
                    instance.cancel()
            except TransitionNotAllowed:
                raise APIValidationError({
                    'status': "The payment could not be transitioned to '{}' "
                              "status.".format(status)
                })

        return super(PaymentSerializer, self).update(instance, validated_data)


class UserArchitectureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserArchitectures
        fields = ('id', 'username', 'arch_name', 'price',)

class Billing_ArchitectureTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Billing_ArchitectureType
        fields = ('id', 'archtype',)

class ArchitectureSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Billing_Architecture
        fields = ('id', 'architecture_name','description','architecture_img','archtype')

class FeatureArchitectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing_FeatureArchitecture
        fields = ('id', 'architecture_name','feature_img','description','architecture_id')

class LoadBalencerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoadBalencer
        fields = ('id','region','ostype','name', 'unit', 'price_per_unit', 'included_units',
                  'EBS_volume','Elastic_IP','termstype','PriceDescription','EffectiveDate','currency','LeaseContractLength','PurchaseOption','OfferingClass',
                  'Product_Family','serviceCode','Location_Type','Instance_Type','Current_Generation','Instance_Family','vCPU',
                  'Physical_Processor','Clock_Speed','Memory','Storage','Network_Performance','Processor_Architecture','Storage_Media',
                  'Volume_Type','Max_Volume_Size','Max_IOPS_volume','Max_IOPS_Burst_Performance','Max_throughput_volume','Provisioned','Tenancy','EBS_Optimized','Operating_System','License_Model','Group',
                  'Group_Description','Transfer_Type','From_Location','From_Location_Type','To_Location','To_Location_Type',
                  'usageType','operation','Dedicated_EBS_Throughput','Enhanced_Networking_Supported','GPU','Instance_Capacity_10xlarge','Instance_Capacity_2xlarge','Instance_Capacity_4xlarge','Instance_Capacity_8xlarge',
                  'Instance_Capacity_large','Instance_Capacity_medium','Instance_Capacity_xlarge','Intel_AVX_Available','Intel_AVX2_Available','Intel_Turbo_Available','Physical_Cores','Pre_Installed_SW','Processor_Features','Sockets')

class S3StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = S3Storage
        fields = ('SKU', 'OfferTermCode', 'RateCode', 'termstype', 'PriceDescription', 'EffectiveDate', 'StartingRange', 'EndingRange', 'Unit', 'price_per_unit', 'currency', 'Product_Family', 'serviceCode', 'region', 'Location_Type', 'Availability', 'Storage_class', 'Volume_Type', 'Fee_Code', 'Fee_Description', 'Group', 'Group_Description', 'Transfer_Type', 'From_Location', 'From_Location_Type', 'To_Location', 'To_Location_Type', 'usageType', 'operation', 'Durability')


class RDSSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RDS
        fields = ('termstype', 'PriceDescription', 'EffectiveDate', 'unit','price_per_unit', 'currency', 'LeaseContractLength','PurchaseOption', 'OfferingClass',  'Product_Family', 'StartingRange', 'EndingRange',   'RelatedTo',   'serviceCode', 'region', 'Location_Type', 'Instance_Type', 'Current_Generation', 'Instance_Family', 'vCPU', 'Physical_Processor', 'Clock_Speed', 'Memory', 'Storage', 'Network_Performance', 'Processor_Architecture', 'engine_code', 'Database_Engine', 'Database_Edition', 'License_Model', 'Deployment_Option', 'Transfer_Type', 'From_Location', 'From_Location_Type', 'To_Location', 'To_Location_Type', 'usageType', 'operation', 'Dedicated_EBS_Throughput', 'Enhanced_Networking_Supported', 'Processor_Features')

class ArchPlanSerializer(serializers.HyperlinkedModelSerializer):
    product_code = ProductCodeRelatedField()
    class Meta:
        model = Plan
        fields = ('product_code','total_plan_price',
                  'instance_count','rds_count','s3_count','balancer_count','instance_name',
                    'rds_name','balancer_name','instance_cost','rds_cost',
                    'loadbalancer_cost','s3_cost','s3_name')

