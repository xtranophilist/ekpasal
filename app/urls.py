from django.conf.urls import patterns, include, url
from django.contrib import admin

from users import views as users_views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', users_views.index, name='home'),
                       # url(r'^app/', include('app.foo.urls')),

                       url(r'^goms-admin/', include(admin.site.urls)),
)
