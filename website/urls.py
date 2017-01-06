""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

from website.apps.home.views import AboutView
from website.views import test_http_code_500

urlpatterns = [
    url(r'^$', AboutView.as_view(), name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', AboutView.as_view(), name="about"),
    # Test internal server error
    url(r'^test500/$', test_http_code_500, name="test_http_code_500"),
    # robots.txt is implemented as a template because Django can't seem to serve a static file from urls.py
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt")),
    # Please refer to https://docs.djangoproject.com/en/1.8/topics/auth/default/#using-the-views
    # for additional information about using django.contrib.auth.urls
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^home/', include('website.apps.home.urls')),
    # url(r'^simulation/', include('website.apps.simulation.urls')),
]

try:
    # If django_auth_pubtkt is available, add redirect_to_sso to urlpattens
    # In production, this URL will be used as login view (LOGIN_URL)
    from django_auth_pubtkt.views import redirect_to_sso
    urlpatterns += [url(r'^sso/', redirect_to_sso),]
except ImportError:
    pass


# handler404 = TemplateView.as_view(template_name="404.html")
