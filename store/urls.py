from django.conf.urls import patterns, url
from store import views


urlpatterns = patterns('',
                       url(r'^categories/$', views.list_categories, name='list_categories'),

)
