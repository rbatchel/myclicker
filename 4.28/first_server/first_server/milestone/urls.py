from django.conf.urls import patterns, url
from milestone import views
from django.conf import settings


urlpatterns = patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 

	# Login/logout
	('^login/$', 'django.contrib.auth.views.login'),
	('^logout/$', views.logout_page),
	
	# Registration
     (r'^register/', views.register),	

	('^userhome/$', views.userhome),
	('^userhome/update.xml$', views.update_xml),

	('^records/info.xml$', views.info_xml),
	('^records/(\w+)/(\w+)/(\w+)$', views.statistics),

	('^\w+/\w+/\w+/update.xml$', views.update_xml),
	#('^update.xml$', views.update_xml),
	('^(\w+)/(\w+)/(\w+)/$', views.redirect),

	('^$', views.start),
)