from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_site01.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^polls/', include('polls.urls', namespace="polls")),
    #url(r'^polls', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^todo/',  include('todo.urls', namespace='todo')),
)
