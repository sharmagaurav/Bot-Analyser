from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from datetime import datetime, date, timedelta
import time
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

from .models import BadBotsIp, GoodBots, GoodUsers, Suspicious, LogConfig
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.db.models import Count
from django.db import connections

#primary variables for data query
#today = datetime.now()
#today = date.today()- timedelta(days=10)
today = datetime.strptime("2015-08-16 01:01:01", '%Y-%m-%d %H:%M:%S')
today = datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
date_today_str = datetime.strftime(today, '%Y-%m-%d')
date_today = datetime.strptime(date_today_str, '%Y-%m-%d')

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


# Create your views here.
@csrf_exempt
def index(request):
	bad_ip = BadBotsIp.objects.order_by('id').count()
	good_ip = GoodBots.objects.order_by('id').count()
	good_user = GoodUsers.objects.order_by('id').count()
	suspicious_ip = Suspicious.objects.order_by('id').count()

	bad_ip_yesterday = BadBotsIp.objects.filter(date_time__gt=date_time_yesterday).count()
	good_ip_yesterday = GoodBots.objects.filter(date_time__gt=date_time_yesterday).count()
	good_user_yesterday = GoodUsers.objects.filter(date_time__gt=date_time_yesterday).count()
	suspicious_ip_yesterday = Suspicious.objects.filter(date_time__gt=date_time_yesterday).count()

	bad_ip_last_hour = BadBotsIp.objects.filter(date_time__gt=date_time_last_hour).count()
	good_ip_last_hour = GoodBots.objects.filter(date_time__gt=date_time_last_hour).count()
	good_user_last_hour = GoodUsers.objects.filter(date_time__gt=date_time_last_hour).count()
	suspicious_ip_last_hour = Suspicious.objects.filter(date_time__gt=date_time_last_hour).count()

	bad_ip_last_week = BadBotsIp.objects.filter(date_time__gt=last_week_date).count()
	good_ip_last_week = GoodBots.objects.filter(date_time__gt=last_week_date).count()
	good_user_last_week = GoodUsers.objects.filter(date_time__gt=last_week_date).count()
	suspicious_ip_last_week = Suspicious.objects.filter(date_time__gt=last_week_date).count()

	bad_ip_last_month = BadBotsIp.objects.filter(date_time__gt=last_month_date).count()
	good_ip_last_month = GoodBots.objects.filter(date_time__gt=last_month_date).count()
	good_user_last_month = GoodUsers.objects.filter(date_time__gt=last_month_date).count()
	suspicious_ip_last_month = Suspicious.objects.filter(date_time__gt=last_month_date).count()



	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/index1.html')
	context = RequestContext(request,{
		'bad_ip': bad_ip,
		'good_ip': good_ip,
		'good_user': good_user,
		'suspicious_ip': suspicious_ip,
		'bad_ip_yesterday': bad_ip_yesterday,
		'good_ip_yesterday': good_ip_yesterday,
		'good_user_yesterday': good_user_yesterday,
		'suspicious_ip_yesterday': suspicious_ip_yesterday,
		'bad_ip_last_hour': bad_ip_last_hour,
		'good_ip_last_hour': good_ip_last_hour,
		'good_user_last_hour': good_user_last_hour,
		'suspicious_ip_last_hour': suspicious_ip_last_hour,
		'bad_ip_last_month': bad_ip_last_month,
		'good_ip_last_month': good_ip_last_month,
		'good_user_last_month': good_user_last_month,
		'suspicious_ip_last_month': suspicious_ip_last_month,
		'bad_ip_last_week': bad_ip_last_week,
		'good_ip_last_week': good_ip_last_week,
		'good_user_last_week': good_user_last_week,
		'suspicious_ip_last_week': suspicious_ip_last_week,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,
		})
	return HttpResponse(template.render(context))

def good_bot_tables(request,question_id):
	good_ip = GoodBots.objects.all()
	good_ip_yesterday = GoodBots.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')
	good_ip_last_week = GoodBots.objects.filter(date_time__gt=last_week_date).order_by('-hits')
	good_ip_last_hour = GoodBots.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')
	good_ip_last_month = GoodBots.objects.filter(date_time__gt=last_month_date).order_by('-hits')

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
	good_user = GoodUsers.objects.order_by('id')[:1000]
	good_user_last_month = GoodUsers.objects.filter(date_time__gt=last_month_date).order_by('-hits')[:1000]
	good_user_last_hour = GoodUsers.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')[:1000]
	good_user_last_week = GoodUsers.objects.filter(date_time__gt=last_week_date).order_by('-hits')[:1000]
	good_user_yesterday = GoodUsers.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')[:1000]

	last_hour = 1
	yesterday = 2
	last_week = 3
	last_month= 4
	template = loader.get_template('readlog/good_user_table.html')
	context = RequestContext(request,{
		'good_user': good_user,
		'question_id': question_id,
		'good_user_last_month': good_user_last_month,
		'good_user_last_hour': good_user_last_hour,
		'good_user_last_week': good_user_last_week,
		'good_user_yesterday': good_user_yesterday,
		'last_hour' : last_hour,
		'yesterday': yesterday,
		'last_week': last_week,
		'last_month': last_month,

		})
	return HttpResponse(template.render(context))

def bad_ip_tables(request,question_id):
	bad_ip = BadBotsIp.objects.all()
	bad_ip_yesterday = BadBotsIp.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')
	bad_ip_last_hour = BadBotsIp.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')
	bad_ip_last_week = BadBotsIp.objects.filter(date_time__gt=last_week_date).order_by('-hits')
	bad_ip_last_month = BadBotsIp.objects.filter(date_time__gt=last_month_date).order_by('-hits')

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
	suspicious_ip = Suspicious.objects.order_by('id')
	suspicious_ip_yesterday = Suspicious.objects.filter(date_time__gt=date_time_yesterday).order_by('-hits')
	suspicious_ip_last_hour = Suspicious.objects.filter(date_time__gt=date_time_last_hour).order_by('-hits')
	suspicious_ip_last_week = Suspicious.objects.filter(date_time__gt=last_week_date).order_by('-hits')
	suspicious_ip_last_month = Suspicious.objects.filter(date_time__gt=last_month_date).order_by('-hits')

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
	bad_ip = BadBotsIp.objects.filter(id=host_id)
	host_name = BadBotsIp.objects.filter(id=host_id).values('host')
	host_data = LogConfig.objects.all().filter(host=host_name).values('endpoint').annotate(total = Count('endpoint')).order_by('-total')[:5]
	user_agent_data = LogConfig.objects.all().filter(host=host_name).values('user_agents').annotate(total = Count('user_agents')).order_by('-total')[:5]
	section_data = LogConfig.objects.all().filter(host=host_name).values('section').annotate(total = Count('section')).order_by('-total')[:5]
	peak_activity = LogConfig.objects.extra(select={'hour': connections[LogConfig.objects.db].ops.date_trunc_sql('hour', 'date_time')}).filter(host=host_name).values('hour').annotate(total = Count('date_time')).order_by('-total')[:5]
	
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

@csrf_exempt
def x(request):
	return HttpResponse("ssjcs")

@csrf_exempt
def logouts(request):
	auth.logout(request)
	return HttpResponseRedirect('/readlog/login/')