from django.conf.urls import patterns, url
from milestone import views


urlpatterns = patterns('',
	# Login/logout
	('^login/$', 'django.contrib.auth.views.login'),
	('^logout/$', views.logout_page),
	
	# Registration
     (r'^register/', views.register),	

	('^student/$', views.student),
	('^student/update.xml$', views.update_xml),

	('^professor/$', views.professor),
	('^professor/update.xml$', views.update_xml),

	('^hello/$', views.hello),
	('^javascript/$', views.trial),
	('^mile0/$', views.noxml),
	('^milestone/$', views.xml),
	('^milestone/update.xml$', views.update_xml),
	('^update$', views.update_xml),
	('^database/$', views.database),

	('^userhome/$', views.userhome),
	('^userhome/update.xml$', views.update_xml),

	('^userhome/(\w+)/$', views.redirect),

)