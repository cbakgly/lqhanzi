# -*- coding:utf8 -*-
"""mysite URL Configuration

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

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from django.views.generic.base import RedirectView
from settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_URL
from hanzi.views.help import help

admin.autodiscover()

urlpatterns = [
    url(r'^', include('hanzi.urls')),
    url(r'^workbench/', include('workbench.urls')),
    url(r'^sysadmin/', include('sysadmin.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=STATIC_URL + 'img/favicon.ico', permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api/(?P<version>\w+)/', include('backend.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^help/', help, name='m1.help'),
]

if DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
