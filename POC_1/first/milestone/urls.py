from django.conf.urls import patterns, url

from milestone import views

urlpatterns = patterns('',
	('^hello/$', views.hello),
	('^javascript/$', views.trial),
	('^mile0/$', views.noxml),
	('^milestone/$', views.xml),
	('^milestone/update.xml$', views.update_xml),
	('^update$', views.update_xml),
	('^database/$', views.database),
)