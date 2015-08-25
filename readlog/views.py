from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from datetime import datetime, date, timedelta
import time
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

from .models import BadBotsIp_test, GoodBots_test, GoodUsers, Suspicious_test, LogConfig_test, logconfig_test_dump
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.db.models import Count
from django.db import connections

#primary variables for data query
today = datetime.now()
# today = date.today()
#today = datetime.strptime("2015-08-24 01:01:01", '%Y-%m-%d %H:%M:%S')
today = datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
date_today_str = datetime.strftime(today, '%Y-%m-%d')
date_today = datetime.strptime(date_today_str, '%Y-%m-%d')
# today = date.today()

#for last_hour
check = date_today_str + " 01:00:00"
check = datetime.strptime(check, '%Y-%m-%d %H:%M:%S')
check = today - check
check = str(date_today_str + " " + str(check))
date_time_last_hour = datetime.strptime(check, '%Y-%m-%d %H:%M:%S')

#for yesterday
yesterday_date = str(date.today()- timedelta(days=1))
yesterday_date += " 00:00:00"
date_time_yesterday = datetime.strptime(yesterday_date, '%Y-%m-%d %H:%M:%S')

#for last week
last_week_date = str(date.today()- timedelta(days=7))
last_week_date += " 00:00:00"
last_week_date = datetime.strptime(last_week_date, '%Y-%m-%d %H:%M:%S')

#for last month
this_month = str(date.today())
this_month = int(this_month[8]+this_month[9])
last_month_date = str(date.today()- timedelta(days=this_month-1)) + " 00:00:00"
last_month_date = datetime.strptime(last_month_date, '%Y-%m-%d %H:%M:%S')


date_five =last_month_date + timedelta(days = 4)
date_ten = last_month_date + timedelta(days= 9)
date_15  = last_month_date + timedelta(days=14)
date_20  = last_month_date + timedelta(days=19)
date_25  = last_month_date + timedelta(days=24)
date_30  = last_month_date + timedelta(days=29)


# Create your views here.
@csrf_exempt
def index(request):
	bad_ip = BadBotsIp_test.objects.order_by('id').count()
	good_ip = GoodBots_test.objects.order_by('id').count()
	#good_user = GoodUsers_test.objects.order_by('id').count()
	suspicious_ip = Suspicious_test.objects.order_by('id').count()

	bad_ip_yesterday = BadBotsIp_test.objects.filter(date_time__gt=date_time_yesterday).count()
	good_ip_yesterday = GoodBots_test.objects.filter(date_time__gt=date_time_yesterday).count()
	#good_user_yesterday = GoodUsers_test.objects.filter(date_time__gt=date_time_yesterday).count()
	suspicious_ip_yesterday = Suspicious_test.objects.filter(date_time__gt=date_time_yesterday).count()
	hits_yesterday = logconfig_test_dump.objects.values('host').filter(date_time__gt=date_time_yesterday).distinct().count()

	bad_ip_last_hour = BadBotsIp_test.objects.filter(date_time__gt=date_time_last_hour).count()
	good_ip_last_hour = GoodBots_test.objects.filter(date_time__gt=date_time_last_hour).count()
	#good_user_last_hour = GoodUsers_test.objects.filter(date_time__gt=date_time_last_hour).count()
	suspicious_ip_last_hour = Suspicious_test.objects.filter(date_time__gt=date_time_last_hour).count()
	hits_last_hour = logconfig_test_dump.objects.values('host').filter(date_time__gt=date_time_last_hour).distinct().count()

	bad_ip_last_week = BadBotsIp_test.objects.filter(date_time__gt=last_week_date).count()
	good_ip_last_week = GoodBots_test.objects.filter(date_time__gt=last_week_date).count()
	#good_user_last_week = GoodUsers_test.objects.filter(date_time__gt=last_week_date).count()
	suspicious_ip_last_week = Suspicious_test.objects.filter(date_time__gt=last_week_date).count()
	hits_last_week = logconfig_test_dump.objects.values('host').filter(date_time__gt=last_week_date).distinct().count()

	bad_ip_last_month = BadBotsIp_test.objects.filter(date_time__gt=last_month_date).count()
	good_ip_last_month = GoodBots_test.objects.filter(date_time__gt=last_month_date).count()
	#good_user_last_month = GoodUsers_test.objects.filter(date_time__gt=last_month_date).count()
	suspicious_ip_last_month = Suspicious_test.objects.filter(date_time__gt=last_month_date).count()
	hits_last_month = logconfig_test_dump.objects.filter(date_time__gt=last_month_date).values('host').distinct().count()

	bad_hosts = BadBotsIp_test.objects.all()
	bad_bots_first = logconfig_test_dump.objects.filter(host__in=bad_hosts, date_time=date_five).count()
	good_bots_first = GoodBots_test.objects.filter(date_time=date_five).count()



	mn = datetime.now()
	mn = mn.strftime("%B")

	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/index1.html')
	context = RequestContext(request,{
		'bad_ip': bad_ip,
		'good_ip': good_ip,
		#'good_user': good_user,
		'suspicious_ip': suspicious_ip,
		'bad_ip_yesterday': bad_ip_yesterday,
		'good_ip_yesterday': good_ip_yesterday,
		#'good_user_yesterday': good_user_yesterday,
		'suspicious_ip_yesterday': suspicious_ip_yesterday,
		'bad_ip_last_hour': bad_ip_last_hour,
		'good_ip_last_hour': good_ip_last_hour,
		#'good_user_last_hour': good_user_last_hour,
		'suspicious_ip_last_hour': suspicious_ip_last_hour,
		'bad_ip_last_month': bad_ip_last_month,
		'good_ip_last_month': good_ip_last_month,
		#'good_user_last_month': good_user_last_month,
		'suspicious_ip_last_month': suspicious_ip_last_month,
		'bad_ip_last_week': bad_ip_last_week,
		'good_ip_last_week': good_ip_last_week,
		#'good_user_last_week': good_user_last_week,
		'suspicious_ip_last_week': suspicious_ip_last_week,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,
		'mn' : mn,
		'hits_yesterday': hits_yesterday,
		'hits_last_hour' : hits_last_hour,
		'hits_last_month' : hits_last_month,
		'hits_last_week' : hits_last_week,
		'bad_bots_first' : bad_bots_first,
		'good_bots_first' : good_bots_first
		})
	return HttpResponse(template.render(context))

def good_bot_tables(request,question_id):
	good_ip = GoodBots_test.objects.all()
	good_ip_yesterday = GoodBots_test.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')
	good_ip_last_week = GoodBots_test.objects.filter(date_time__gt=last_week_date).order_by('-hits')
	good_ip_last_hour = GoodBots_test.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')
	good_ip_last_month = GoodBots_test.objects.filter(date_time__gt=last_month_date).order_by('-hits')

	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/good_bot_table.html')
	context = RequestContext(request,{
		'good_ip': good_ip,
		'question_id': question_id,
		'good_ip_yesterday': good_ip_yesterday,
		'good_ip_last_month': good_ip_last_month,
		'good_ip_last_week': good_ip_last_week,
		'good_ip_last_hour': good_ip_last_hour,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,

		})
	return HttpResponse(template.render(context))

def good_user_tables(request,question_id):
	# good_user = GoodUsers_test.objects.order_by('id')[:1000]
	# good_user_last_month = GoodUsers_test.objects.filter(date_time__gt=last_month_date).order_by('-hits')[:1000]
	# good_user_last_hour = GoodUsers_test.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')[:1000]
	# good_user_last_week = GoodUsers_test.objects.filter(date_time__gt=last_week_date).order_by('-hits')[:1000]
	# good_user_yesterday = GoodUsers_test.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')[:1000]

	# last_hour = 1
	# yesterday = 2
	# last_week = 3
	# last_month= 4
	# template = loader.get_template('readlog/good_user_table.html')
	# context = RequestContext(request,{
	# 	'good_user': good_user,
	# 	'question_id': question_id,
	# 	'good_user_last_month': good_user_last_month,
	# 	'good_user_last_hour': good_user_last_hour,
	# 	'good_user_last_week': good_user_last_week,
	# 	'good_user_yesterday': good_user_yesterday,
	# 	'last_hour' : last_hour,
	# 	'yesterday': yesterday,
	# 	'last_week': last_week,
	# 	'last_month': last_month,

	# 	})
	return HttpResponse(template.render(context))

def bad_ip_tables(request,question_id):
	bad_ip = BadBotsIp_test.objects.all()
	bad_ip_yesterday = BadBotsIp_test.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')
	bad_ip_last_hour = BadBotsIp_test.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')
	bad_ip_last_week = BadBotsIp_test.objects.filter(date_time__gt=last_week_date).order_by('-hits')
	bad_ip_last_month = BadBotsIp_test.objects.filter(date_time__gt=last_month_date).order_by('-hits')

	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/bad_ip_tables.html')
	context = RequestContext(request,{
		'bad_ip': bad_ip,
		'question_id': question_id,
		'bad_ip_yesterday': bad_ip_yesterday,
		'bad_ip_last_hour': bad_ip_last_hour,
		'bad_ip_last_week': bad_ip_last_week,
		'bad_ip_last_month': bad_ip_last_month,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,

		})
	return HttpResponse(template.render(context))

def suspicious_ip_tables(request,question_id):
	suspicious_ip = Suspicious_test.objects.order_by('id')
	suspicious_ip_yesterday = Suspicious_test.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')
	suspicious_ip_last_hour = Suspicious_test.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')
	suspicious_ip_last_week = Suspicious_test.objects.filter(date_time__gt=last_week_date).order_by('-hits')
	suspicious_ip_last_month = Suspicious_test.objects.filter(date_time__gt=last_month_date).order_by('-hits')

	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/suspicious_ip_tables.html')
	context = RequestContext(request,{
		'suspicious_ip': suspicious_ip,
		'question_id': question_id,
		'suspicious_ip_yesterday': suspicious_ip_yesterday,
		'suspicious_ip_last_hour': suspicious_ip_last_hour,
		'suspicious_ip_last_week': suspicious_ip_last_week,
		'suspicious_ip_last_month': suspicious_ip_last_month,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,

		})
	return HttpResponse(template.render(context))

@csrf_exempt
def logins(request):
	template = loader.get_template('readlog/login.html')
	state = "Please log in below..."
	username = password = ''
	if request.POST:
	    username = request.POST.get('username')
	    password = request.POST.get('password')

	    user = authenticate(username=username, password=password)
	    if user is not None:
	        if user.is_active:
	            login(request, user)
	            state = "You're successfully logged in!"
	            return HttpResponseRedirect('/readlog/')
	        else:
	            state = "Your account is not active, please contact the site admin."
	    else:
	        state = "Your username and/or password were incorrect."

	context = RequestContext(request,{
	    	'state':state, 
	    	'username': username,
		})
	return HttpResponse(template.render(context))


def bad_ip_details(request, question_id, host_id):
	bad_ip = BadBotsIp_test.objects.filter(id=host_id)
	host_name = BadBotsIp_test.objects.filter(id=host_id).values('host')
	host_data = logconfig_test_dump.objects.all().filter(host=host_name).values('endpoint').annotate(total = Count('endpoint')).order_by('-total')[:5]
	user_agent_data = logconfig_test_dump.objects.all().filter(host=host_name).values('user_agents').annotate(total = Count('user_agents')).order_by('-total')[:5]
	section_data = logconfig_test_dump.objects.all().filter(host=host_name).values('section').annotate(total = Count('section')).order_by('-total')[:5]
	peak_activity = logconfig_test_dump.objects.extra(select={'hour': connections[logconfig_test_dump.objects.db].ops.date_trunc_sql('hour', 'date_time')}).filter(host=host_name).values('hour').annotate(total = Count('date_time')).order_by('-total')[:5]
	
	template = loader.get_template('readlog/login.html')
	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/bad_ip_details.html')
	context = RequestContext(request,{
		'peak_activity' : peak_activity,
		'section_data' : section_data,
		'user_agent_data' : user_agent_data,
		'host_data' : host_data,
		'bad_ip' : bad_ip,
		'question_id' : question_id,
		'host_id' : host_id,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,

		})
	return HttpResponse(template.render(context))

def suspicious_ip_details(request, question_id, host_id):
	bad_ip = Suspicious_test.objects.filter(id=host_id)
	host_name = Suspicious_test.objects.filter(id=host_id).values('host')
	host_data = logconfig_test_dump.objects.all().filter(host=host_name).values('endpoint').annotate(total = Count('endpoint')).order_by('-total')[:5]
	user_agent_data = logconfig_test_dump.objects.all().filter(host=host_name).values('user_agents').annotate(total = Count('user_agents')).order_by('-total')[:5]
	section_data = logconfig_test_dump.objects.all().filter(host=host_name).values('section').annotate(total = Count('section')).order_by('-total')[:5]
	peak_activity = logconfig_test_dump.objects.extra(select={'hour': connections[logconfig_test_dump.objects.db].ops.date_trunc_sql('hour', 'date_time')}).filter(host=host_name).values('hour').annotate(total = Count('date_time')).order_by('-total')[:5]
	
	template = loader.get_template('readlog/login.html')
	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/suspicious_ip_details.html')
	context = RequestContext(request,{
		'peak_activity' : peak_activity,
		'section_data' : section_data,
		'user_agent_data' : user_agent_data,
		'host_data' : host_data,
		'bad_ip' : bad_ip,
		'question_id' : question_id,
		'host_id' : host_id,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,

		})
	return HttpResponse(template.render(context))

@csrf_exempt
def x(request):
	return HttpResponse("ssjcs")

@csrf_exempt
def logouts(request):
	auth.logout(request)
	return HttpResponseRedirect('/readlog/login/')