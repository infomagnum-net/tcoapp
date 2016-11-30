"""cloudtco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import *  # NOQA
  
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tco/', include('tcoapp.urls'),name="tcoapp"),
    url(r'^', include('tco.urls'),name="tco"),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^silver/', include('silver.api.urls')),
    url(r'^accounts/', include('allauth.urls')),
    #url(r'^tco/', include('tcoapp.urls'),name="tcoapp"),
 ]

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'tcoapp.views.custom_404'

# # This is only needed when using runserver.

# if settings.DEBUG and not urlpatterns:
#     urlpatterns += staticfiles_urlpatterns()


# if settings.DEBUG:
#     urlpatterns = patterns('',
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
#             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#         ) + staticfiles_urlpatterns() + urlpatterns  # NOQA


# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
#     urlpatterns += patterns('',
#             url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )