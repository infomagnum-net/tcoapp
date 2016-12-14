from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^logout/$', views.logout_page, name="logout_page"),
    url(r'^conformation/$', views.payment_conformation, name='payment_conformation'),
    url(r'^application/$', views.application, name='application'),
    url(r'^verticals/$', views.verticals, name='verticals'),
    url(r'^profile/$', views.Profile, name="Profile"),
    url(r'^editprofile/$', views.edit, name="edit"),
    url(r'^help/$', views.help, name="help"),
    url(r'^warning/$', views.warning, name="warning"),
    url(r'^simple/$', views.simple_upload, name='simple_upload'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^monitoring/$', views.monitoring, name='monitoring'),
    url(r'^404/$',views.handler404,name="handler404" ),
    url(r'^architecture/$', views.rest_main_architectures, name='rest_main_architectures'),
    url(r'^complete-arch-info/(?P<pk>[0-9]+)/$', views.rest_arch_complete_info, name='rest_arch_complete_info'),
    url(r'^ftrd-for-arch/(?P<pk>[0-9]+)/$', views.FtrdArchForArch, name='FtrdArchForArch'),
    url(r'^ftrd-cmplt-info/(?P<pk>[0-9]+)/$', views.CompleteFtrdArchInfo, name='CompleteFtrdArchInfo'),
    url(r'^planspage/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.planspage, name='planspage'),
    url(r'^invoice/(?P<name>[A-Za-z0-9\w@%._ -]+)/(?P<plan_type>[A-Za-z0-9\w@%._ -]+)/$', views.invoicepage, name='invoicepage'),
    url(r'^launch-img/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.Launch_img, name='arch_with_plansinfo'),
    url(r'^payment/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.PayementPlans, name='PayementPlans'),
    url(r'^ftrd_popup/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.Featured_model_popup, name='Featured_model_popup'),
    url(r'^chat-store/$', views.chat_conversation, name='chat_conversation'),
    url(r'^app_popup/$', views.app_popup, name="app_popup"),
    url(r'^ftrd_popup/(?P<name>[A-Za-z0-9\w@%._ -]+)/$', views.Featured_model_popup, name='Featured_model_popup'),
    url(r'^check/$', views.check, name="check"),



    url(r'^host_step1/$', views.host_step1, name='host_step1'),
    url(r'^host_step2/$', views.host_step2, name='host_step2'),
    url(r'^host_step3/$', views.host_step3, name='host_step3'),
    url(r'^host_step4/$', views.host_step4, name='host_step4'),
    url(r'^host_step5/$', views.host_step5, name='host_step5'),
    url(r'^host_step6/$', views.host_step6, name='host_step6'),
    url(r'^host_step7/$', views.host_step7, name='host_step7'),   
    url(r'^step7_53host/$', views.step7_53host, name='step7_53host'),   
    url(r'^step7_cleanup_cloudfront/$', views.step7_cleanup_cloudfront, name='step7_cleanup_cloudfront'),
    url(r'^step7_cleanup_s3/$', views.step7_cleanup_s3, name='step7_cleanup_s3'),

]