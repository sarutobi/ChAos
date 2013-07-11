# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from profile.views import CreateUser

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'ChAos.views.home', name='home'),
    # url(r'^ChAos/', include('ChAos.foo.urls')),
    url(r'^$', 'challenge.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    # Account manipulations
    url('^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login_form.html', }),
    url(r'^accounts/profile/$', 'challenge.views.index'),
    url(r'^accounts/register/$', CreateUser.as_view()),
    url('^challenge/', include('challenge.urls')),
)
