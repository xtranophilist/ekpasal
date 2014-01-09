from django.conf.urls import patterns, url
from store import views


urlpatterns = patterns('',
                       url(r'^categories/$', views.list_categories, name='list_categories'),
                       url(r'^category/(?P<slug>[a-zA-Z0-9_.-]+)$', views.view_category, name='view_category'),

)
