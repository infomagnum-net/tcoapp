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


from django.conf.urls import patterns, url
from silver import views as silver_views
from silver.api import views

urlpatterns = [
    url(r'^customers/$',
        views.CustomerList.as_view(), name='customer-list'),

    url(r'^launched-architectures/$',
        views.UserArchitectureList.as_view(), name='launched-architectures'),

    url(r'^architectures/$',
        views.ArchitectureList.as_view(), name='architectures-list'),

    url(r'^ftrdarchitectures/$',
        views.FeatureArchitectureList.as_view(), name='Ftrdarchitectures-list'),

    url(r'^architecture-types/$',
        views.ArchitectureType.as_view(), name='ArchitectureType-list'),

    url(r'^loadbalancer/$',
        views.LoadBalencerList.as_view(), name='LoadBalencerList-list'),

    url(r'^s3/$',
        views.S3StorageList.as_view(), name='S3StorageList-list'),

    url(r'^rds/$',
        views.RDSList.as_view(), name='RDSList-list'),


    url(r'plans/(?P<pk>[0-9]+)/rds/$',
        views.PlanRDS.as_view(), name='PlanRDS'),

    url(r'plans/(?P<pk>[0-9]+)/s3/$',
        views.PlanS3.as_view(), name='PlanS3'),

    url(r'plans/load-balancer/$',
        views.PlanLoadbalancer.as_view(), name='PlanS3'),

    # url(r'^user-architectures/$',
    #     views.UserArchitectureList.as_view(), name='customer-list'),


    url(r'^customers/(?P<pk>[0-9]+)/$',
        views.CustomerDetail.as_view(), name='customer-detail'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/subscriptions/$',
        views.SubscriptionList.as_view(), name='subscription-list'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/subscriptions/(?P<subscription_pk>[0-9]+)/$',
        views.SubscriptionDetail.as_view(), name='subscription-detail'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/subscriptions/(?P<subscription_pk>[0-9]+)/metered-features/(?P<mf_product_code>([^/])+)/$',
        views.MeteredFeatureUnitsLogDetail.as_view(), name='mf-log-units'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/subscriptions/(?P<subscription_pk>[0-9]+)/activate/$',
        views.SubscriptionActivate.as_view(), name='sub-activate'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/subscriptions/(?P<subscription_pk>[0-9]+)/cancel/$',
        views.SubscriptionCancel.as_view(), name='sub-cancel'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/subscriptions/(?P<subscription_pk>[0-9]+)/reactivate/$',
        views.SubscriptionReactivate.as_view(), name='sub-reactivate'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/payments/$',
        views.PaymentList.as_view(), name='payment-list'),
    url(r'^customers/(?P<customer_pk>[0-9]+)/payments/(?P<payment_pk>[0-9]+)/$',
        views.PaymentDetail.as_view(), name='payment-detail'),
    url(r'^plans/$',
        views.PlanList.as_view(), name='plan-list'),
    url(r'^plans/(?P<pk>[0-9]+)/$',
        views.PlanDetail.as_view(), name='plan-detail'),
    url(r'plans/(?P<pk>[0-9]+)/metered-features/$',
        views.PlanMeteredFeatures.as_view(), name='plans-metered-features'),
    url(r'^metered-features/$',
        views.MeteredFeatureList.as_view(), name='metered-feature-list'),
    url(r'^providers/$',
        views.ProviderListCreate.as_view(), name='provider-list'),
    url(r'^providers/(?P<pk>[0-9]+)/$',
        views.ProviderRetrieveUpdateDestroy.as_view(), name='provider-detail'),
    url(r'^product-codes/$',
        views.ProductCodeListCreate.as_view(), name='productcode-list'),
    url(r'^product-codes/(?P<pk>[0-9]+)/$',
        views.ProductCodeRetrieveUpdate.as_view(), name='productcode-detail'),
    url(r'^invoices/$',
        views.InvoiceListCreate.as_view(), name='invoice-list'),
    url(r'^invoices/(?P<pk>[0-9]+)/$',
        views.InvoiceRetrieveUpdate.as_view(), name='invoice-detail'),
    url(r'^invoices/(?P<document_pk>[0-9]+)/entries/$',
        views.InvoiceEntryCreate.as_view(), name='invoice-entry-create'),
    url(r'^invoices/(?P<document_pk>[0-9]+)/entries/(?P<entry_pk>[0-9]+)/$',
        views.InvoiceEntryUpdateDestroy.as_view(), name='invoice-entry-update'),
    url(r'^invoices/(?P<pk>[0-9]+)/state/$',
        views.InvoiceStateHandler.as_view(), name='invoice-state'),
    url(r'^invoices/(?P<invoice_id>\d+).pdf$',
        silver_views.invoice_pdf, name='invoice-pdf'),
    url(r'^proformas/$',
        views.ProformaListCreate.as_view(), name='proforma-list'),
    url(r'^proformas/(?P<pk>[0-9]+)/$',
        views.ProformaRetrieveUpdate.as_view(), name='proforma-detail'),
    url(r'^proformas/(?P<document_pk>[0-9]+)/entries/$',
        views.ProformaEntryCreate.as_view(), name='proforma-entry-create'),
    url(r'^proformas/(?P<document_pk>[0-9]+)/entries/(?P<entry_pk>[0-9]+)/$',
        views.ProformaEntryUpdateDestroy.as_view(),
        name='proforma-entry-update'),
    url(r'^proformas/(?P<pk>[0-9]+)/state/$',
        views.ProformaStateHandler.as_view(), name='proforma-state'),
    url(r'^proformas/(?P<pk>[0-9]+)/invoice/$',
        views.ProformaInvoiceRetrieveCreate.as_view(),
        name='proforma-invoice'),
    url(r'^proformas/(?P<proforma_id>\d+).pdf$',
        silver_views.proforma_pdf, name='proforma-pdf'),
    url(r'^getxls/$',silver_views.getxls, name='getxls'),
    url(r'^store/$',silver_views.store_data, name='store_data'),
    url(r'^csv_data/$',silver_views.csv_data, name='csv_data'),
    url(r'^rds/$',silver_views.rds_data, name='rds_data'),
    url(r'^s3storage/$',silver_views.s3storage, name='s3storage'),
    url(r'^architecture/(?P<pk>[0-9]+)/$',
        views.ArhitectureByID.as_view(), name='ArhitectureByID'),
    url(r'^my-own-view/$', views.MyOwnView.as_view(),name='my-own-view'),
    url(r'^product-codes/(?P<pk>[0-9]+)/$',
        views.ProductCodeByID.as_view(), name='ProductCodeByID'),
    url(r'^plans/(?P<name>[A-Za-z0-9\w@%._ -]+)/$',
        views.PlanByArchName.as_view(), name='PlanByArchName'),
    url(r'^arch-complete-info/(?P<pk>[0-9]+)/$',
        views.ArchCompleInfo.as_view(), name='ArchCompleInfo'),
    url(r'^featured-arch/(?P<pk>[0-9]+)/$',
        views.FtrdArchByArchID.as_view(), name='FtrdArchByArchID'),
    url(r'^featured-arch-complete-info/(?P<pk>[0-9]+)/$',
        views.FtrdArchCompleInfo.as_view(), name='FtrdArchCompleInfo'),
    
    url(r'^arch/(?P<name>[A-Za-z0-9\w@%._ -]+)/$',
        views.Architectures_by_name.as_view(), name='Architectures_by_name'),
    

    # url(r'^invoice/(?P<name>[A-Za-z0-9\w@%._ -]+)/$',
    #     views.InvoicePage.as_view(), name='InvoicePage'),

    
    
    

    


]


