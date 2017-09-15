"""Djago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from Yq_Djago.mytrip import tripviews
from Yq_Djago.loginsys import loginviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^trip/$', tripviews.hello),
    url(r'^$', loginviews.login),
    url(r'^homepage$', loginviews.homepage),
    url(r'^forreturn/$', loginviews.returndata),
    url(r'^getinterface/$', loginviews.getinterface),
    url(r'^getinterfacepayload/$', loginviews.getinterfacepayload),

    # url(r'^', views.hello),
    # url(r'^yqji', search.yqji),
    # url(r'^search-form$', search.search_form),
    # url(r'^search$', search.search),
]
