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


class BadBotsIp(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256, default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime

class GoodBots(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime

class GoodUsers(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime

class Suspicious(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime

class Unknown(models.Model):
	host             = models.CharField(max_length=100) #127.0.0.1
	Description      = models.CharField(max_length=256,default="")
	date_time        = models.DateTimeField(default="1900-01-01 00:00:00")	          #Datetime
	
class Rules(models.Model):
	Description      = models.CharField(max_length=256,default="")