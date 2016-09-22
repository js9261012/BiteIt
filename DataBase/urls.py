from django.conf.urls import patterns, url

from DataBase import views

urlpatterns = patterns('',

	url(r'^$', views.requestMap, name='requestMap'),
	url(r'^showStoreInfo/$', views.showStoreInfo, name='showStoreInfo'),
	url(r'^showMappingLocation/$', views.showMappingLocation, name='showMappingLocation'),
	url(r'^showNotQueryLocation/$', views.showNotQueryLocation, name='showNotQueryLocation'),
	url(r'^list/$', views.listall, name='list'),

)