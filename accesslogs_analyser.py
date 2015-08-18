#! /usr/bin/env python
import os
import MySQLdb
import re
from datetime import datetime
import time

dic = {
	'Jan': '01',
	'Feb': '02',
	'Mar': '03',
	'Apr': '04',
	'May': '05',
	'Jun': '06',
	'Jul': '07',
	'Oct': '10',
	'Nov': '11',
	'Dec': '12',
	'Aug': '08',
	'Sep': '09',
}

bad_bots  = []
good_bots = []


def preliminary_test():
	"""
	This evaluates whether the request contains a user agent
	or not. 
	"""
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	p = "-"
	description_bad_ip = 'Empty user agent'
	description_good_ip = 'Ajax requests'
	cursor.execute("SELECT distinct(host), date_time from readlog_logconfig  where user_agents like %s group by host",(p))

	data = cursor.fetchall()
	count = 0
	temp = []
	for row in data:
		ip = data[count]
		temp.append(ip)
		count+=1
	# cursor.execute("SELECT distinct(host), date_time from readlog_logconfig  where endpoint like '%ajax%' group by host")
	# data2 = cursor.fetchall()
	# temp2 = []
	# count = 0
	# for row in data2:
	# 	ip = data2[count]
	# 	temp2.append(ip)
	# 	count+=1
	print len(temp)
	for i in range(len(temp)):
		cursor.execute("SELECT count(*) from readlog_logconfig where host = %s",temp[i][0])
		c1 = cursor.fetchall()
		hits = c1[0][0]
		# print i+1, ": ", hits
		cursor.execute("INSERT INTO readlog_badbotsip (host, Description, date_time, hits) VALUES (%s,%s,%s,%s)",(str(temp[i][0]), description_bad_ip, temp[i][1], hits))

	# for i in range(len(temp2)):
	# 	cursor.execute("INSERT INTO readlog_goodusers (host, Description, date_time) VALUES (%s,%s,%s)",(str(temp2[i][0]), description_good_ip, temp2[i][1]))
	local_host = """('127.0.0.1',)"""
	cursor.execute("delete from readlog_badbotsip where host = %s",(local_host))
	conn.commit()
	print "Preliminary test done."


def excess_requests_in_recent_past():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	cursor.execute("SELECT distinct(host) from readlog_badbotsip")
	data = cursor.fetchall()
	b = set(data)
	x = list(b)
	xx = []
	for i in range(len(x)):
		xx.append(x[i][0])


	cursor.execute("SELECT distinct(host) from readlog_goodbots")
	data = cursor.fetchall()
	g = set(data)
	y = list(g)
	yy = []

	for i in range(len(y)):
		yy.append(y[i][0])


	cursor.execute("SELECT distinct(host) from readlog_goodusers")
	data = cursor.fetchall()
	u = set(data)
	z = list(u)
	zz = []

	for i in range(len(z)):
		zz.append(z[i][0])
	
	cursor.execute("SELECT host, count(*) as c from readlog_logconfig group by host order by c desc limit 2000")
	data = cursor.fetchall()
	t = set(data)
	w = list(t)
	s = []
	
	for i in range(len(w)):
		s.append(w[i][0])

	ff = set(xx)|set(yy)|set(zz)
	#print len(xx),"+",len(yy),"+",len(zz),"=",len(ff)

	fff = set(s) & set(ff)
	#print len(fff)

	ffff = set(s) - set(fff)

	#print len(ffff)

	distinct_host_list = list(ffff)
	#print distinct_host_list[0]
	print "Distinct hosts : ",len(distinct_host_list)

	suspicious_ip = []
	host_ip_count = []

	dts_list = []
	for i in range(len(distinct_host_list)):
		host_ip = str(distinct_host_list[i])
		cursor.execute("SELECT max(date_time) from readlog_logconfig where host = %s",(distinct_host_list[i]))
		
		data = cursor.fetchone()
		y = data[0]
		x = str(data[0])
		p = x.split()
		pre = datetime.strptime(p[1],"%H:%M:%S")
		sub = datetime.strptime("01:00","%M:%S")
		dif = pre-sub
		dif = str(dif)
		final = p[0] + 	" " + dif
		
		cursor.execute("SELECT host, count(*) as c from readlog_logconfig where host = %s and date_time > %s",(host_ip, final))
		p1 = cursor.fetchall()

		if(p1[0][1]>=20):	
			crumb = host_ip
			suspicious_ip.append(crumb)
			dts_list.append(y)
			host_ip_count.append(p1[0][1])

	
	print "Suspicious ips: ",len(suspicious_ip)
	for i in range(len(suspicious_ip)):
		#cursor.execute("INSERT INTO readlog_suspicious (host) VALUES (%s)",(str(suspicious_ip[i])))
		cursor.execute("INSERT INTO readlog_suspicious (host, Description, date_time, hits) VALUES (%s,%s,%s,%s)",(suspicious_ip[i], "Excess access in one minute", dts_list[i], host_ip_count[i]))

	conn.commit()

	print "Excess access done."



def botAndIp():

	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()


	a=['%googlebot%','%rogerbot/1.0%', '%Mozilla/xintellibot%','%Twitterbot%', '%bitlybot%', '%bitlybot/2.0%', '%msnbot%','%bingbot%']
	b=['66.249.6','209.133.111.215|208.184.81.30|61.194.12.33' , '194.90.251.114|194.90.251.117|194.90.251.115|194.90.251.113|194.90.251.116' , '149.154.167|199.16.156.124|199.16.156.125|199.16.156.126|199.59.148.209|199.59.148.210|199.59.148.211|199.59.149.21|199.59.149.45', '23.21.3.171|54.237.43.151|50.17.151.94|50.17.69.56|107.20.32.80|54.227.49.251|54.198.188.134|54.224.44.111|54.235.40.139|184.72.158.161','54.147.4.25|50.19.1.73|54.242.155.200|184.72.159.8', '65.55|65.54|131.107|157.55|202.96.51|199.30.17','65.52.104|65.52.108|65.55.24|65.55.52|65.55.55|65.55.213|65.55.217|131.253.24|131.253.46|157.55.16|157.55.18|157.55.32|157.55.36|157.55.48|157.55.109|157.55.110|157.55.110|157.56.92|157.56.93|157.56.94|157.56.229|199.30.16|207.46.12.|207.46.192|207.46.195|207.46.199|207.46.204|157.55.39|207.46.13']
	length = len(a)

	desc=['googlebot','rogerbot/1.0','Mozilla/xintellibot','Twitterbot', 'bitlybot', 'bitlybot/2.0','msnbot','bingbot']
	count = 0
	
	for i in range(length):
		temp = []
		hitslist = []
		cursor.execute("select distinct(host), date_time, count(*) from readlog_logconfig where user_agents like %s and host REGEXP %s group by host",(a[i],b[i]))
		data= cursor.fetchall()
		date_list = []
		print a[i]," : ",len(data)
		
		for x  in range(len(data)):
			temp.append(data[x][0])
			date_list.append(data[x][1])
			hitslist.append(data[x][2])
		
		for i in range(len(temp)):

			cursor.execute("INSERT INTO readlog_goodbots (host, Description, date_time, hits) VALUES (%s,%s,%s,%s)",(temp[i], desc[count], date_list[i], hitslist[i]))

		count+=1

	conn.commit()
	print "Good bots done"

def scrappers():

	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()


	a1='Offline Explorer|SiteSnagger|WebCopier|WebReaper|WebStripper|WebZIP|TeleportPro|Xaldon_WebSpider'
	a = 'Offline Explorer'	
	
	cursor.execute("select distinct(host), user_agents, date_time from readlog_logconfig where user_agents REGEXP %s group by host",(a))
	data= cursor.fetchall()
	
	for i in range(len(data)):
		ips = str(data[i][0])
		scr = str(data[i][1])
		dts = data[i][2]
		des = scr + " Scrapper"


		cursor.execute("SELECT count(*) from readlog_logconfig where host = %s",ips)
		c1 = cursor.fetchall()
		hits = c1[0][0]

		cursor.execute("INSERT INTO readlog_badbotsip (host, Description, date_time, hits) VALUES (%s,%s,%s,%s)",(ips,des,dts, hits))

	conn.commit()
	print "Scrappers found"

def badbot_agents():

	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()

	b = ['MJ12bot','ia_archiver|nutch|AhrefsBot','Python-urllib|oBot','UniversalFeedParser|DigExt']
	gg = set()
	for i in range(4):
		cursor.execute("select distinct(host), date_time from readlog_logconfig where user_agents REGEXP %s group by host",(b[i]))
		data= cursor.fetchall()
		
		print len(data)
		for x in range(len(data)):
			ips = str(data[x][0])
			scr = b[i]
			dts = data[x][1]
			des = str(scr) + " Bot"

			cursor.execute("SELECT count(*) from readlog_logconfig where host = %s",ips)
			c1 = cursor.fetchall()
			hits = c1[0][0]

			cursor.execute("INSERT INTO readlog_badbotsip (host, Description, date_time, hits) VALUES (%s,%s,%s,%s)",(ips,des,dts,hits))

	conn.commit()

def check():
	start = time.time()
	print start
	preliminary_test()
	botAndIp()
	scrappers()
	badbot_agents()
	excess_requests_in_recent_past()
	end = time.time()
	print end - start

if __name__ == '__main__':
	check()