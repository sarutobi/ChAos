from django.conf.urls import patterns, include, url

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
    url('^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login_form.html', }),
    url(r'^accounts/profile/$', 'challenge.views.index'),
    url('^challenge/', include('challenge.urls'))
)
