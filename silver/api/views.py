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


import datetime
import logging
from decimal import Decimal

from django.http.response import Http404
from django.utils import timezone
from rest_framework import generics, permissions, status, filters
from rest_framework.generics import (get_object_or_404, ListCreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateAPIView
from annoying.functions import get_object_or_None

from silver.models import (MeteredFeatureUnitsLog, Subscription, MeteredFeature,
                           Customer, Plan, Provider, Invoice, ProductCode,
                           DocumentEntry, Proforma, BillingDocument, Payment)

from silver.models.billing_entities.base import UserArchitectures

from silver.models.product_codes import Billing_ArchitectureType,Billing_Architecture,Billing_FeatureArchitecture


from silver.api.serializers import (MFUnitsLogSerializer,
                                    CustomerSerializer, SubscriptionSerializer,
                                    SubscriptionDetailSerializer,
                                    PlanSerializer, MeteredFeatureSerializer,
                                    ProviderSerializer, InvoiceSerializer,
                                    ProductCodeSerializer, ProformaSerializer,
                                    DocumentEntrySerializer, PaymentSerializer,
                                    UserArchitectureSerializer,
                                    Billing_ArchitectureTypeSerializer,
                                    ArchitectureSerializer,
                                    FeatureArchitectureSerializer,
                                    LoadBalencerSerializer,
                                    S3StorageSerializer,
                                    RDSSerializer,
                                    ArchPlanSerializer,)
from silver.api.filters import (MeteredFeaturesFilter, SubscriptionFilter,
                                CustomerFilter, ProviderFilter, PlanFilter,
                                InvoiceFilter, ProformaFilter, PaymentFilter)
from silver.models.plans import Region,RDS,S3Storage,LoadBalencer
from django.http import HttpResponse
import json
from django.shortcuts import render, redirect, render_to_response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
import requests
from django.core import serializers
logger = logging.getLogger(__name__)


class PlanList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlanFilter


class PlanDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlanSerializer
    model = Plan

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        return get_object_or_404(Plan, pk=pk)

    def patch(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan.objects, pk=self.kwargs.get('pk', None))
        name = request.data.get('name', None)
        generate_after = request.data.get('generate_after', None)
        plan.name = name or plan.name
        plan.generate_after = generate_after or plan.generate_after
        plan.save()
        return Response(PlanSerializer(plan, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan.objects, pk=self.kwargs.get('pk', None))
        plan.enabled = False
        plan.save()
        return Response({"deleted": not plan.enabled},
                        status=status.HTTP_200_OK)





    # def get_queryset(self):
    #     plan = get_object_or_None(Plan, pk=self.kwargs['pk'])    
    #     return  plan.LoadBalencer_metered.all() if plan else None
    



class MeteredFeatureList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MeteredFeatureSerializer
    queryset = MeteredFeature.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MeteredFeaturesFilter


class MeteredFeatureDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MeteredFeatureSerializer
    model = MeteredFeature

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        return get_object_or_404(MeteredFeature, pk=pk)


class SubscriptionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SubscriptionFilter

    def get_queryset(self):
        customer_pk = self.kwargs.get('customer_pk', None)
        queryset = Subscription.objects.filter(customer__id=customer_pk)
        return queryset.order_by('start_date')

    def post(self, request, *args, **kwargs):
        customer_pk = self.kwargs.get('customer_pk', None)
        url = reverse('customer-detail', kwargs={'pk': customer_pk},
                      request=request)
        request.data.update({unicode('customer'): unicode(url)})

        return super(SubscriptionList, self).post(request, *args, **kwargs)


class SubscriptionDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionDetailSerializer

    def get_object(self):
        customer_pk = self.kwargs.get('customer_pk', None)
        subscription_pk = self.kwargs.get('subscription_pk', None)
        return get_object_or_404(Subscription, customer__id=customer_pk,
                                 pk=subscription_pk)

    def put(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PUT" not allowed.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        sub = get_object_or_404(Subscription.objects,
                                pk=self.kwargs.get('subscription_pk', None))
        state = sub.state
        meta = request.data.pop('meta', None)
        if request.data:
            message = "Cannot update a subscription when it's in %s state." \
                      % state
            return Response({"detail": message},
                            status=status.HTTP_400_BAD_REQUEST)
        request.data.clear()
        request.data.update({'meta': meta} if meta else {})
        return super(SubscriptionDetail, self).patch(request,
                                                     *args, **kwargs)


class SubscriptionActivate(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        sub = get_object_or_404(Subscription.objects,
                                pk=self.kwargs.get('subscription_pk', None))
        if sub.state != Subscription.STATES.INACTIVE:
            message = 'Cannot activate subscription from %s state.' % sub.state
            return Response({"error": message},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.POST.get('_content', None):
                start_date = request.data.get('start_date', None)
                trial_end = request.data.get('trial_end_date', None)
                if start_date:
                    try:
                        start_date = datetime.datetime.strptime(
                            start_date, '%Y-%m-%d').date()
                    except TypeError:
                        return Response(
                            {'detail': 'Invalid start_date date format. Please '
                                       'use the ISO 8601 date format.'},
                            status=status.HTTP_400_BAD_REQUEST)
                if trial_end:
                    try:
                        trial_end = datetime.datetime.strptime(
                            trial_end, '%Y-%m-%d').date()
                    except TypeError:
                        return Response(
                            {'detail': 'Invalid trial_end date format. Please '
                                       'use the ISO 8601 date format.'},
                            status=status.HTTP_400_BAD_REQUEST)
                sub.activate(start_date=start_date, trial_end_date=trial_end)
                sub.save()
            else:
                sub.activate()
                sub.save()

            logger.debug('Activated subscription: %s', {
                'subscription': sub.id,
                'date': timezone.now().date().strftime('%Y-%m-%d')
            })

            return Response({"state": sub.state},
                            status=status.HTTP_200_OK)


class SubscriptionCancel(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        sub = get_object_or_404(Subscription,
                                pk=kwargs.get('subscription_pk', None))
        when = request.data.get('when', None)
        if sub.state != Subscription.STATES.ACTIVE:
            message = 'Cannot cancel subscription from %s state.' % sub.state
            return Response({"error": message},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if when in [Subscription.CANCEL_OPTIONS.NOW,
                        Subscription.CANCEL_OPTIONS.END_OF_BILLING_CYCLE]:
                sub.cancel(when=when)
                sub.save()

                logger.debug('Canceled subscription: %s', {
                    'subscription': sub.id,
                    'date': timezone.now().date().strftime('%Y-%m-%d'),
                    'when': when,
                })

                return Response({"state": sub.state},
                                status=status.HTTP_200_OK)
            else:
                if when is None:
                    err = 'You must provide the `when` argument'
                    return Response({'error': err},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    err = 'You must provide a correct value for the `when` argument'
                    return Response({'error': err},
                                    status=status.HTTP_400_BAD_REQUEST)


class SubscriptionReactivate(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        sub = get_object_or_404(Subscription,
                                pk=kwargs.get('subscription_pk', None))
        if sub.state != Subscription.STATES.CANCELED:
            msg = 'Cannot reactivate subscription from %s state.' % sub.state
            return Response({"error": msg},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            sub.activate()
            sub.save()

            logger.debug('Reactivated subscription: %s', {
                'subscription': sub.id,
                'date': timezone.now().date().strftime('%Y-%m-%d'),
            })

            return Response({"state": sub.state},
                            status=status.HTTP_200_OK)


class MeteredFeatureUnitsLogDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = None

    def get(self, request, format=None, **kwargs):
        subscription_pk = kwargs.get('subscription_pk', None)
        mf_product_code = kwargs.get('mf_product_code', None)

        subscription = Subscription.objects.get(pk=subscription_pk)

        metered_feature = get_object_or_404(
            subscription.plan.metered_features,
            product_code__value=mf_product_code
        )

        logs = MeteredFeatureUnitsLog.objects.filter(
            metered_feature=metered_feature.pk,
            subscription=subscription_pk)

        serializer = MFUnitsLogSerializer(
            logs, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        mf_product_code = self.kwargs.get('mf_product_code', None)
        subscription_pk = self.kwargs.get('subscription_pk', None)

        try:
            subscription = Subscription.objects.get(pk=subscription_pk)
        except Subscription.DoesNotExist:
            return Response({"detail": "Subscription Not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # TODO: change this to try-except
        metered_feature = get_object_or_None(
            subscription.plan.metered_features,
            product_code__value=mf_product_code
        )

        if not metered_feature:
            return Response({"detail": "Metered Feature Not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if subscription.state != 'active':
            return Response({"detail": "Subscription is not active."},
                            status=status.HTTP_403_FORBIDDEN)

        required_fields = ['date', 'count', 'update_type']
        provided_fields = {}
        errors = {}
        for field in required_fields:
            try:
                provided_fields[field] = request.data[field]
            except KeyError:
                errors[field] = ["This field is required."]

        for key in provided_fields:
            if not provided_fields[key]:
                errors[key] = ["This field may not be blank."]

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        date = request.data['date']
        consumed_units = request.data['count']
        update_type = request.data['update_type']

        consumed_units = Decimal(consumed_units)

        try:
            date = datetime.datetime.strptime(date,
                                              '%Y-%m-%d').date()
        except TypeError:
            return Response({'detail': 'Invalid date format. Please '
                            'use the ISO 8601 date format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if date < subscription.start_date:
            return Response({"detail": "Date is out of bounds."},
                            status=status.HTTP_400_BAD_REQUEST)

        bsd = subscription.bucket_start_date(date)
        bed = subscription.bucket_end_date(date)
        if not bsd or not bed:
            return Response(
                {'detail': 'An error has been encountered.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        interval = next(
            (i for i in subscription.updateable_buckets()
                if i['start_date'] == bsd and i['end_date'] == bed),
            None)

        if interval is None:
            return Response({"detail": "Date is out of bounds."},
                            status=status.HTTP_400_BAD_REQUEST)

        if metered_feature not in \
                subscription.plan.metered_features.all():
            err = "The metered feature does not belong to the " \
                  "subscription's plan."
            return Response(
                {"detail": err},
                status=status.HTTP_400_BAD_REQUEST
            )

        log = MeteredFeatureUnitsLog.objects.filter(
            start_date=bsd,
            end_date=bed,
            metered_feature=metered_feature.pk,
            subscription=subscription_pk
        ).first()

        if log is not None:
            if update_type == 'absolute':
                log.consumed_units = consumed_units
            elif update_type == 'relative':
                log.consumed_units += consumed_units
            log.save()
        else:
            log = MeteredFeatureUnitsLog.objects.create(
                metered_feature=metered_feature,
                subscription=subscription,
                start_date=bsd,
                end_date=bed,
                consumed_units=consumed_units
            )
        return Response({"count": log.consumed_units},
                        status=status.HTTP_200_OK)


class CustomerList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    serializer_class = CustomerSerializer
    
    queryset = Customer.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CustomerFilter



class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        pk = self.kwargs.get('pk', None)
        try:
            return Customer.objects.get(pk=pk)
        except (TypeError, ValueError, Customer.DoesNotExist):
            raise Http404

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerSerializer
    model = Customer


class ProductCodeListCreate(generics.ListCreateAPIView):
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductCodeSerializer
    queryset = ProductCode.objects.all()


class ProductCodeRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductCodeSerializer
    queryset = ProductCode.objects.all()


class ProviderListCreate(ListBulkCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProviderFilter


class ProviderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()


class InvoiceListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = InvoiceFilter


class InvoiceRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


class DocEntryCreate(generics.CreateAPIView):
    def get_model(self):
        raise NotImplementedError

    def get_model_name(self):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        doc_pk = kwargs.get('document_pk')
        Model = self.get_model()
        model_name = self.get_model_name()

        try:
            document = Model.objects.get(pk=doc_pk)
        except Model.DoesNotExist:
            msg = "{model} not found".format(model=model_name)
            return Response({"detail": msg}, status=status.HTTP_404_NOT_FOUND)

        if document.state != BillingDocument.STATES.DRAFT:
            msg = "{model} entries can be added only when the {model_lower} is"\
                  " in draft state.".format(model=model_name,
                                            model_lower=model_name.lower())
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = DocumentEntrySerializer(data=request.data,
                                             context={'request': request})

        if serializer.is_valid(raise_exception=True):
            # This will be eiter {invoice: <invoice_object>} or
            # {proforma: <proforma_object>} as a DocumentEntry can have a
            # foreign key to either an invoice or a proforma
            extra_context = {model_name.lower(): document}
            serializer.save(**extra_context)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvoiceEntryCreate(DocEntryCreate):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DocumentEntrySerializer
    queryset = DocumentEntry.objects.all()

    def post(self, request, *args, **kwargs):
        return super(InvoiceEntryCreate, self).post(request, *args, **kwargs)

    def get_model(self):
        return Invoice

    def get_model_name(self):
        return "Invoice"


class DocEntryUpdateDestroy(APIView):

    def put(self, request, *args, **kwargs):
        doc_pk = kwargs.get('document_pk')
        entry_pk = kwargs.get('entry_pk')

        Model = self.get_model()
        model_name = self.get_model_name()

        document = get_object_or_404(Model, pk=doc_pk)
        if document.state != BillingDocument.STATES.DRAFT:
            msg = "{model} entries can be added only when the {model_lower} is"\
                  " in draft state.".format(model=model_name,
                                            model_lower=model_name.lower())
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)

        searched_fields = {model_name.lower(): document, 'pk': entry_pk}
        entry = get_object_or_404(DocumentEntry, **searched_fields)

        serializer = DocumentEntrySerializer(entry, data=request.data,
                                             context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        doc_pk = kwargs.get('document_pk')
        entry_pk = kwargs.get('entry_pk')

        Model = self.get_model()
        model_name = self.get_model_name()

        document = get_object_or_404(Model, pk=doc_pk)
        if document.state != BillingDocument.STATES.DRAFT:
            msg = "{model} entries can be deleted only when the {model_lower} is"\
                  " in draft state.".format(model=model_name,
                                            model_lower=model_name.lower())
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)

        searched_fields = {model_name.lower(): document, 'pk': entry_pk}
        entry = get_object_or_404(DocumentEntry, **searched_fields)
        entry.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_model(self):
        raise NotImplementedError

    def get_model_name(self):
        raise NotImplementedError


class InvoiceEntryUpdateDestroy(DocEntryUpdateDestroy):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DocumentEntrySerializer
    queryset = DocumentEntry.objects.all()

    def put(self, request, *args, **kwargs):
        return super(InvoiceEntryUpdateDestroy, self).put(request, *args,
                                                          **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(InvoiceEntryUpdateDestroy, self).delete(request, *args,
                                                             **kwargs)

    def get_model(self):
        return Invoice

    def get_model_name(self):
        return "Invoice"


class InvoiceStateHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InvoiceSerializer

    def put(self, request, *args, **kwargs):
        invoice_pk = kwargs.get('pk')
        try:
            invoice = Invoice.objects.get(pk=invoice_pk)
        except Invoice.DoesNotExist:
            return Response({"detail": "Invoice not found"},
                            status=status.HTTP_404_NOT_FOUND)

        state = request.data.get('state', None)
        if state == Invoice.STATES.ISSUED:
            if invoice.state != Invoice.STATES.DRAFT:
                msg = "An invoice can be issued only if it is in draft state."
                return Response({"detail": msg},
                                status=status.HTTP_403_FORBIDDEN)

            issue_date = request.data.get('issue_date', None)
            due_date = request.data.get('due_date', None)
            invoice.issue(issue_date, due_date)
            invoice.save()
        elif state == Invoice.STATES.PAID:
            if invoice.state != Invoice.STATES.ISSUED:
                msg = "An invoice can be paid only if it is in issued state."
                return Response({"detail": msg},
                                status=status.HTTP_403_FORBIDDEN)

            paid_date = request.data.get('paid_date', None)
            invoice.pay(paid_date)
            invoice.save()
        elif state == Invoice.STATES.CANCELED:
            if invoice.state != Invoice.STATES.ISSUED:
                msg = "An invoice can be canceled only if it is in issued " \
                      "state."
                return Response({"detail": msg},
                                status=status.HTTP_403_FORBIDDEN)

            cancel_date = request.data.get('cancel_date', None)
            invoice.cancel(cancel_date)
            invoice.save()
        elif not state:
            msg = "You have to provide a value for the state field."
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)
        else:
            msg = "Illegal state value."
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = InvoiceSerializer(invoice, context={'request': request})
        return Response(serializer.data)


class ProformaListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProformaSerializer
    queryset = Proforma.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProformaFilter


class ProformaRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProformaSerializer
    queryset = Proforma.objects.all()


class ProformaEntryCreate(DocEntryCreate):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DocumentEntrySerializer
    queryset = DocumentEntry.objects.all()

    def post(self, request, *args, **kwargs):
        return super(ProformaEntryCreate, self).post(request, *args, **kwargs)

    def get_model(self):
        return Proforma

    def get_model_name(self):
        return "Proforma"


class ProformaEntryUpdateDestroy(DocEntryUpdateDestroy):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DocumentEntrySerializer
    queryset = DocumentEntry.objects.all()

    def put(self, request, *args, **kwargs):
        return super(ProformaEntryUpdateDestroy, self).put(request, *args,
                                                           **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(ProformaEntryUpdateDestroy, self).delete(request, *args,
                                                              **kwargs)

    def get_model(self):
        return Proforma

    def get_model_name(self):
        return "Proforma"


class ProformaInvoiceRetrieveCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InvoiceSerializer

    def post(self, request, *args, **kwargs):
        proforma_pk = kwargs.get('pk')

        try:
            proforma = Proforma.objects.get(pk=proforma_pk)
        except Proforma.DoesNotExist:
            return Response({"detail": "Proforma not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if not proforma.invoice:
            proforma.create_invoice()

        serializer = InvoiceSerializer(proforma.invoice,
                                       context={'request': request})
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        proforma_pk = kwargs.get('pk')

        try:
            proforma = Proforma.objects.get(pk=proforma_pk)
        except Proforma.DoesNotExist:
            return Response({"detail": "Proforma not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(proforma.invoice,
                                       context={'request': request})
        return Response(serializer.data)


class ProformaStateHandler(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProformaSerializer

    def put(self, request, *args, **kwargs):
        proforma_pk = kwargs.get('pk')
        try:
            proforma = Proforma.objects.get(pk=proforma_pk)
        except Proforma.DoesNotExist:
            return Response({"detail": "Proforma not found"},
                            status=status.HTTP_404_NOT_FOUND)

        state = request.data.get('state', None)
        if state == Proforma.STATES.ISSUED:
            if proforma.state != Proforma.STATES.DRAFT:
                msg = "A proforma can be issued only if it is in draft state."
                return Response({"detail": msg},
                                status=status.HTTP_403_FORBIDDEN)

            issue_date = request.data.get('issue_date', None)
            due_date = request.data.get('due_date', None)
            proforma.issue(issue_date, due_date)
            proforma.save()
        elif state == Proforma.STATES.PAID:
            if proforma.state != Proforma.STATES.ISSUED:
                msg = "A proforma can be paid only if it is in issued state."
                return Response({"detail": msg},
                                status=status.HTTP_403_FORBIDDEN)

            paid_date = request.data.get('paid_date', None)
            proforma.pay(paid_date)
            proforma.save()
        elif state == Proforma.STATES.CANCELED:
            if proforma.state != Proforma.STATES.ISSUED:
                msg = "A proforma can be canceled only if it is in issued " \
                      "state."
                return Response({"detail": msg},
                                status=status.HTTP_403_FORBIDDEN)

            cancel_date = request.data.get('cancel_date', None)
            proforma.cancel(cancel_date)
            proforma.save()
        elif not state:
            msg = "You have to provide a value for the state field."
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)
        else:
            msg = "Illegal state value."
            return Response({"detail": msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProformaSerializer(proforma, context={'request': request})
        return Response(serializer.data)


class PaymentList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = PaymentFilter
    ordering = ('-due_date',)

    def get_queryset(self):
        customer_pk = self.kwargs.get('customer_pk', None)
        queryset = Payment.objects.filter(customer__id=customer_pk)
        return queryset.order_by('due_date')

    def post(self, request, *args, **kwargs):
        customer_pk = self.kwargs.get('customer_pk', None)
        url = reverse('customer-detail', kwargs={'pk': customer_pk},
                      request=request)
        request.data.update({unicode('customer'): unicode(url)})

        return super(PaymentList, self).post(request, *args, **kwargs)


class PaymentDetail(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get_object(self):
        customer_pk = self.kwargs.get('customer_pk', None)
        payment_pk = self.kwargs.get('payment_pk', None)
        return get_object_or_404(Payment, customer__id=customer_pk,
                                 pk=payment_pk)


class ArchitectureType(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Billing_ArchitectureTypeSerializer
    queryset = Billing_ArchitectureType.objects.all()





# class  ArchitectureList(generics.ListCreateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     #permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = ArchitectureSerializer
#     queryset = Billing_Architecture.objects.filter(archtype="cloud")



class  ArchitectureList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    #permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeatureArchitectureSerializer
    serializer_class = ArchitectureSerializer
    cldtype=Billing_ArchitectureType.objects.filter(archtype="cloud")
    queryset = Billing_Architecture.objects.filter(archtype=cldtype)


class FeatureArchitectureList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeatureArchitectureSerializer
    queryset = Billing_FeatureArchitecture.objects.all()

class LoadBalencerList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LoadBalencerSerializer
    queryset = LoadBalencer.objects.all()

class S3StorageList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = S3StorageSerializer()
    queryset = S3Storage.objects.all()
    
    

class RDSList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RDSSerializer
    queryset = RDS.objects.all()



'''25/11/16 APIL CALLS'''

# class PlanMeteredFeatures(generics.ListAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = MeteredFeatureSerializer
#     model = MeteredFeature


#     def get_queryset(self):
#         plan = get_object_or_None(Plan, pk=self.kwargs['pk'])
#         return plan.metered_features.all() if plan else None


def arch_info_with_name_byname(name):
    dataset={}
    product=ProductCode.objects.filter(value="WP-Model 1")
    arch=Billing_Architecture.objects.filter(architecture_name=product).values('architecture_name','architecture_img','id')
    ftrd_arch=Billing_FeatureArchitecture.objects.filter(architecture_name=product).values("id","architecture_id",
            "feature_img","architecture_name","apptype_img")
    if arch:
        dataset=arch
    else:
        dataset=ftrd_arch
    products=ProductCode.objects.filter(value=name).values("id","value")
    archs=dataset[0]
    prdcts=products[0]
    archs['architecture_name']=prdcts['value']
    return archs


class PlanMeteredFeatures(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MeteredFeatureSerializer
    model = MeteredFeature
    def get_queryset(self):
        plan = get_object_or_None(Plan, pk=self.kwargs['pk'])
        plan_mtrd_ftrs=plan.metered_features.all() if plan else None
        print '***'*20
        print plan_mtrd_ftrs.values_list("price_per_unit")
        return plan_mtrd_ftrs



class UserArchitectureList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        arch=UserArchitectures.objects.filter(username=request.user.username).values('id', 'arch_name', 'price','created_at')
        return Response(arch)


class PlanRDS(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RDSSerializer
    model = RDS
    def get_queryset(self):
        plan = get_object_or_None(Plan, pk=self.kwargs['pk'])
        return plan.rds_metered_feature.all() if plan else None

class PlanS3(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = S3StorageSerializer
    model = S3Storage

    def get_queryset(self):
        plan = get_object_or_None(Plan, pk=self.kwargs['pk'])
        return plan.s3_metered_features.all() if plan else None


class PlanLoadbalancer(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LoadBalencerSerializer
    model = LoadBalencer



class ArhitectureByID(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request,pk):
        arch=Billing_Architecture.objects.filter(id=pk).values('architecture_name','architecture_img','id')
        product=ProductCode.objects.all().values("id","value")
        product_name=""
        for prdct in product:
            if prdct['id']==arch[0]['architecture_name']:
                product_name=prdct['value']
        for a in arch:
            a['architecture_name'] = product_name
        return Response(arch)


class ProductCodeByID(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCodeSerializer
    model = ProductCode
    def get_queryset(self):
        dsds=ProductCode.objects.filter(id=self.kwargs['pk'])
        return dsds


class PlanByArchName(generics.ListCreateAPIView):
    #authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class =ArchPlanSerializer
    model = Plan
    def get_queryset(self):
        print self.kwargs['name']
        prdct=ProductCode.objects.filter(value=self.kwargs['name'])
        dsds=Plan.objects.filter(product_code=prdct)
        return dsds

# class FtrdArchByArchID(generics.ListCreateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = FeatureArchitectureSerializer
#     model = Billing_FeatureArchitecture
#     def get_queryset(self):
#         print self.kwargs['pk']
#         ftrd_arch=Billing_FeatureArchitecture.objects.filter(architecture_id=self.kwargs['pk']).values("id","architecture_id",
#             "feature_img","architecture_name")

#         return ftrd_arch


from itertools import chain
class FtrdArchByArchID(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request,pk):
        ftrd_arch=Billing_FeatureArchitecture.objects.filter(architecture_id=pk).values("id","architecture_id",
            "feature_img","architecture_name","apptype_img",)
        product=ProductCode.objects.all().values("id","value")
        
        for prdct in product:
            for ftrd in ftrd_arch:
                if prdct['id']==ftrd['architecture_name']:
                    ftrd['architecture_name']=prdct['value']
                else:
                    pass

        # archname=""
        # main_arch=Billing_Architecture.objects.filter(id=pk).values('architecture_name','architecture_img','id')
        # for prdct in product:
        #     if prdct['id'] == main_arch[0]['architecture_name'] :
        #         archname=prdct['value']
        #     else:
        #         pass

        # for arch in main_arch:
        #     arch['architecture_name']=archname
        #     arch['main_arch_name']=arch.pop("architecture_name")
        #     arch['main_arch_img']=arch.pop("architecture_img")
        #     arch['main_arch_id']=arch.pop("id")
           
        # result_list = list(chain(ftrd_arch, main_arch))
        return Response(ftrd_arch)




class MyOwnView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        token=Token.objects.get(user_id=request.user.id)
        mytoken=token.key
        cldtype=Billing_ArchitectureType.objects.filter(archtype="cloud")
        queryset = Billing_Architecture.objects.filter(archtype=cldtype).values('architecture_name','architecture_img','id','apptype_img')
        prdct=ProductCode.objects.all().values('id','value')
        for product in prdct:
            for name in queryset:
                if product['id']== name['architecture_name']:
                    name['architecture_name']=product['value']
                else:
                    pass
        return Response(queryset)


class ArchCompleInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request,pk):
        token=Token.objects.get(user_id=request.user.id)
        mytoken=token.key
        arch_info=Billing_Architecture.objects.filter(id=pk).values('architecture_name','architecture_img','id','apptype_img')
        product=ProductCode.objects.filter(id=arch_info[0]["architecture_name"]).values("id",'value')
        arch_info[0]["architecture_name"]=product[0]['value']
        arch=arch_info[0]
        prdct=product[0]
        arch['architecture_name']=prdct['value']
        plan_url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':prdct['value']})
        planinfo=requests.get(plan_url, headers={'Authorization': 'Token {}'.format(mytoken)})
        data1 = arch
        data2 = planinfo.json()[0]
        data1.update(data2)
        return Response(data1)


class FtrdArchCompleInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request,pk):
        token=Token.objects.get(user_id=request.user.id)
        mytoken=token.key
        arch_info=ftrd_arch=Billing_FeatureArchitecture.objects.filter(id=pk).values("id","architecture_id",
            "feature_img","architecture_name","apptype_img")
        product=ProductCode.objects.filter(id=arch_info[0]["architecture_name"]).values("id",'value')
        arch_info[0]["architecture_name"]=product[0]['value']
        arch=arch_info[0]
        prdct=product[0]
        arch['architecture_name']=prdct['value']
        plan_url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':prdct['value']})
        planinfo=requests.get(plan_url, headers={'Authorization': 'Token {}'.format(mytoken)})
        data1 = arch
        data2 = planinfo.json()[0]
        data1.update(data2)
        return Response(data1)


class Architectures_by_name(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request,name):
        product=ProductCode.objects.filter(value=name)
        architecture_info={}
        architecture=Billing_Architecture.objects.filter(architecture_name=product).values('architecture_name','architecture_img','id','apptype_img')
        if architecture:
            architecture_info=architecture
        else:
            architecture_info=Billing_FeatureArchitecture.objects.filter(architecture_name=product).values("id","architecture_id",
            "feature_img","architecture_name",'apptype_img')
        prdct=ProductCode.objects.filter(value=name).values("id",'value')
        for arch in architecture_info:
            arch['architecture_name']=prdct[0]['value']
        return Response(architecture_info)


class AllplansInfo(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class =ArchPlanSerializer
    model = Plan
    def get_queryset(self):
        dsds=Plan.objects.all()
        return dsds