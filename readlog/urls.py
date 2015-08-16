from django.conf.urls import url
from  . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	#url(r'^good_bot_tables/$', views.good_bot_tables, name = 'good_bot_tables'),
	url(r'^(?P<question_id>[0-9]+)/good_bot_tables/$', views.good_bot_tables, name = 'good_bot_tables'),
	url(r'^(?P<question_id>[0-9]+)/good_user_tables/$', views.good_user_tables, name = 'good_user_tables'),	
	url(r'^(?P<question_id>[0-9]+)/bad_ip_tables/$', views.bad_ip_tables, name = 'bad_ip_tables'),
	url(r'^(?P<question_id>[0-9]+)/suspicious_ip_tables/$', views.suspicious_ip_tables, name = 'suspicious_ip_tables'),	
	url(r'^login/$', views.logins, name = 'login'),
	url(r'^logout/$', views.logouts, name='logout'),
	url(r'^(?P<question_id>[0-9]+)/bad_ip_tables/(?P<host_id>[0-9]+)/$', views.bad_ip_details, name = 'bad_ip_tables'),	


]