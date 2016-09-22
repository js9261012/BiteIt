from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BiteIt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^DataBase/', include('DataBase.urls')),
    url(r'^mapping/', include('algorithm.urls'))
)
