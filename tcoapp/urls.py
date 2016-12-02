from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # url(r'^$', views.IndexLogin),
    url(r'^login/$', views.Login, name="Login"),

    url(r'^register/$', views.Register, name="Register"),
    url(r'^forgot/$', views.Forgot, name="Forgot"),
    url(r'^frgotpwd/$', views.Forgotpwd, name="Forgotpwd"),
	url(r'^logout/$', views.logout_page, name="logout_page"),
    url(r'^profile/$', views.Profile, name="Profile"),
    url(r'^editprofile/$', views.edit, name="edit"),
    url(r'^help/$', views.help, name="help"),
    url(r'^simple/$', views.simple_upload, name='simple_upload'),
    url(r'^test/$', views.test, name="test"),
    
    url(r'^application/$', views.application, name='application'),
    url(r'^verticals/$', views.verticals, name='verticals'),
    url(r'^architecture/(?P<img_id>[A-Za-z0-9\w @%&._-]+)/$', views.feature_architecture_view, name='feartures'),
    url(r'^privacy/$', views.resetpwd, name="resetpwd"),
    url(r'^resetpwd-ajax/$', views.resetpwd_ajax, name="resetpwd_ajax"),
    url(r'^architecture/launch/(?P<img_id>[A-Za-z0-9\w @%&._-]+)/$', views.architecture_launch, name='architecture_launch'),    
    url(r'^payment/$', views.payment_view, name='payments'),
    url(r'^plans/$', views.plans_view, name='payments_plans'),
    url(r'^keys/download/$', views.key_download, name='download user access key'),
    url(r'^dynamic-change/$', views.dynamic_image_change, name="dynamic_image_change"),
    url(r'^invoice/$', views.invoice, name='invoice'),
    url(r'^activate/(?P<cnfrm_id>[A-Za-z0-9\w @%&._-]+)/$', views.activate_usr, name='activate_usr'),
    url(r'^launch/acrhitecture/$', views.cloud_process_wizard_view, name='cloud_process_wizard_view'),
    url(r'^featured_img_wzrd/$', views.featured_image_wizard, name='featured_image_wizard'),    
    url(r'^pymnts-wzrd/$', views.payments_wizard, name='payments_wizard'),
    url(r'^invoce_wizard/$', views.invoce_wizard, name='invoce_wizard'),
    url(r'^invoice-to-info/$', views.invoice_info, name='invoice_info'),
    url(r'^sendemail/$', views.sendemail, name='sendemail'),
    url(r'^billing-payment/$', views.billing_payment, name='billing_payment'),
    url(r'^instance-launch/$', views.instance_launch, name='instance_launch'),
    url(r'^404/$',views.handler404,name="handler404" ),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^monitoring/$', views.monitoring, name='monitoring'),
    url(r'^testingapi/$', views.testingapi, name='testingapi'),
    url(r'^testwizard/$', views.testwizard, name='testwizard'),
    url(r'^conformation/$', views.payment_conformation, name='payment_conformation'),
    url(r'^404/$',views.handler404,name="handler404" ),
    url(r'^architecture/$', views.rest_main_architectures, name='rest_main_architectures'),
    url(r'^complete-arch-info/(?P<pk>[0-9]+)/$', views.rest_arch_complete_info, name='rest_arch_complete_info'),
    url(r'^ftrd-for-arch/(?P<pk>[0-9]+)/$', views.FtrdArchForArch, name='FtrdArchForArch'),
    url(r'^ftrd-cmplt-info/(?P<pk>[0-9]+)/$', views.CompleteFtrdArchInfo, name='CompleteFtrdArchInfo'),
    url(r'^planspage/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.planspage, name='planspage'),
    url(r'^invoice/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.invoicepage, name='invoicepage'),
    url(r'^launch-img/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.Launch_img, name='arch_with_plansinfo'),
    url(r'^payment/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.PayementPlans, name='PayementPlans'),
    url(r'^ftrd_popup/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.Featured_model_popup, name='Featured_model_popup'),
]