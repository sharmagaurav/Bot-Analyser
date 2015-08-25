from django.db import models

# Create your models here.

class LogConfig(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	client_id        = models.CharField(max_length=100)
	user_id          = models.CharField(max_length=100)
	date_time        = models.DateTimeField()	          #Datetime
	method           = models.CharField(max_length=256) #GET, POST
	endpoint         = models.CharField(max_length=256) #admin/login/?next=/admin/
	protocol         = models.CharField(max_length=256) #HTTP/1.1
	response_code    = models.CharField(max_length=256) #200 status code
	content_size     = models.CharField(max_length=256) #1305
	user_agents      = models.CharField(max_length=256, default="") #user agent with header
	mobile           = models.IntegerField(default=0)
	user_agents_flag = models.IntegerField(default=0)
	section          = models.CharField(max_length=256, default="")


class BadBotsIp(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256, default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class GoodBots(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class GoodUsers(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class Suspicious(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class Unknown(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)
	
class Rules(models.Model):
	Description      = models.CharField(max_length=256,default="")

class Feature_vector(models.Model):
	host             = models.CharField(max_length=100)
	no_of_requests   = models.FloatField(default=0)
	no_of_sections   = models.FloatField(default=0)
	avg_session_time = models.FloatField(default=0)
	hits_per_session = models.FloatField(default=0)
	time_bw_requests = models.FloatField(default=0)
	sessions_per_day = models.FloatField(default=0)


class LogConfig_test(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	client_id        = models.CharField(max_length=100)
	user_id          = models.CharField(max_length=100)
	date_time        = models.DateTimeField()	          #Datetime
	method           = models.CharField(max_length=256) #GET, POST
	endpoint         = models.CharField(max_length=256) #admin/login/?next=/admin/
	protocol         = models.CharField(max_length=256) #HTTP/1.1
	response_code    = models.CharField(max_length=256) #200 status code
	content_size     = models.CharField(max_length=256) #1305
	user_agents      = models.CharField(max_length=256, default="") #user agent with header
	mobile           = models.IntegerField(default=0)
	user_agents_flag = models.IntegerField(default=0)
	section          = models.CharField(max_length=256, default="")


class GoodBots_test(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class Suspicious_test(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class BadBotsIp_test(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256, default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	hits             = models.IntegerField(default=0)

class logconfig_test_dump(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	client_id        = models.CharField(max_length=100)
	user_id          = models.CharField(max_length=100)
	date_time        = models.DateTimeField()	          #Datetime
	method           = models.CharField(max_length=256) #GET, POST
	endpoint         = models.CharField(max_length=256) #admin/login/?next=/admin/
	protocol         = models.CharField(max_length=256) #HTTP/1.1
	response_code    = models.CharField(max_length=256) #200 status code
	content_size     = models.CharField(max_length=256) #1305
	user_agents      = models.CharField(max_length=256, default="") #user agent with header
	mobile           = models.IntegerField(default=0)
	user_agents_flag = models.IntegerField(default=0)
	section          = models.CharField(max_length=256, default="")

class training_centroids(models.Model):
	Description = models.CharField(max_length=256)
	centroid1   = models.FloatField(default=0.0)
	centroid2   = models.FloatField(default=0.0)
	centroid3   = models.FloatField(default=0.0)
	count       = models.IntegerField(default=0)
	deviation   = models.FloatField(default=0.0)
	distance    = models.FloatField(default=0.0)
