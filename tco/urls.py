from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', views.login, name='login'),
    # url(r'^testing/$', views.Testing, name='Testing'),

]

