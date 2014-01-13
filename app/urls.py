from django.conf.urls import patterns, include, url
from django.contrib import admin

from users import views as users_views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:

                       # (r'^user/', include('users.urls')),
                       # url(r'^app/', include('app.foo.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       # (r'^search/', include('haystack.urls')),
                       url(r'', include('store.urls')),
)
