#!/usr/bin/env python
import os
import subprocess
import re
import MySQLdb
from subprocess import Popen, PIPE, STDOUT
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

def bulk_insert_logs_2(host_list,client_id_list,user_id_list,
			date_time_list,method_list,endpoint_list,protocol_list,
			response_code_list,content_size_list,user_agents_list,
			mobile_list,user_agent_flag_list,section_list,left):
	
	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()
	try:
		for i in range(left):
			cursor.execute("INSERT INTO readlog_logconfig_test (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i], section_list[i]))
			cursor.execute("INSERT INTO readlog_logconfig_test_dump (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i], section_list[i]))
	except:
		pass
	conn.commit()


def bulk_insert_logs(host_list,client_id_list,user_id_list,
			date_time_list,method_list,endpoint_list,protocol_list,
			response_code_list,content_size_list,user_agents_list,
			mobile_list,user_agent_flag_list,section_list):
	
	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()
	try:
		for i in range(5000):
			cursor.execute("INSERT INTO readlog_logconfig_test (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i], section_list[i]))
			cursor.execute("INSERT INTO readlog_logconfig_test_dump (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i], section_list[i]))
	except:
		pass
	conn.commit()


def get_old_access_logs():
	old_log_pattern = '^\[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s*" (\d{3}) (\S+) (\S+) (\S+) (.*$)'
	date_res = "([^:]+):(\d+:\d+:\d+) ([^\]]+)"

	path = r'access-test'
	for dir_entry in os.listdir(path):
	    dir_entry_path = os.path.join(path, dir_entry)
	    if os.path.isfile(dir_entry_path):
	        with open(dir_entry_path, 'r') as f:
				#f = open('/home/gaurav/myproject/30_access.log','r')
				count = 0
				text = f.readlines()
				f.close()

				num_lines = sum(1 for line in open(dir_entry_path,'r'))
				print num_lines

				host_list              = []
				client_id_list         = []
				user_id_list           = []
				date_time_list         = []
				method_list            = []
				endpoint_list          = []
				protocol_list          = []
				response_code_list     = []
				content_size_list      = []
				user_agents_list       = []
				mobile_list            = []
				user_agent_flag_list   = []
				section_list           = []


				#f = open("/home/gaurav/myproject/readlog/testlogs.txt",'a')
				while count<num_lines:
					
					req = text[count]
					m = re.findall ( 'httpd: (.*?) -', req, re.DOTALL)
					p = re.findall('- - (.*$)',req,re.DOTALL)
					
					try:
						matchObj = re.match(old_log_pattern,p[0], re.M|re.I)
					except:
						count+=1
					mobile_string = "Mobile"
					mobile_string_present = 0
					t = "-"
					print count+1
					if matchObj:
						if len(m)==0:
							pass
						else:
							temp_host = [x.strip() for x in m[0].split(',')]
							if(temp_host[0]=='127.0.0.1' and len( temp_host)>1):
								host1      = temp_host[1]
							else:
								host1      = temp_host[0]
							client_id2     = t
							client_id2 = str(client_id2)
							user_id3       = '-'
							date_time4     = matchObj.group(1)
							method5        = matchObj.group(2)
							endpoint6      = matchObj.group(3)
							protocol7      = matchObj.group(4)
							response_code8 = matchObj.group(5)
							content_size9  = matchObj.group(6)
							h = matchObj.group(9)
							m = h.split('"')
							user_agents10  = matchObj.group(8) + " " + m[0]
							if ('"-"' in user_agents10):
								user_agents10 = '-'
								print user_agents10
							user_agent_string = str(user_agents10)
							
							user_agent_flag = 0
							if(user_agents10):
								user_agent_flag = 1

							if mobile_string in user_agent_string:
								mobile_string_present = 1
							
							mobile11 = mobile_string_present
							temp_section = endpoint6.split('/')
							if(temp_section[1] == ''):
								section11 = "/" + temp_section[1]
							else:
								section11 = "/" + temp_section[1] + "/"

							temp = re.match(date_res,date_time4, re.M|re.I)
							x1 = temp.group(1)
							x2 = temp.group(2)
							x3 = temp.group(3)
							x4 = x1.split('/')
							x4[1] = dic[x4[1]]

							x5 = x4[1] + " " + x4[0] + " " + x4[2] + " " + x2

							date_time4 = datetime.strptime(x5,'%m %d %Y %H:%M:%S')
							dates = str(date_time4)
							mobiles = str(mobile11)
							flag = str(user_agent_flag)

							line_to_parse = host1 + " " + client_id2 + " " + user_id3 + " " + dates + " " + method5 + " " + endpoint6 + " " + protocol7 + " " + response_code8 + " " + content_size9 + " " + user_agents10 + " " + mobiles + " " + flag

							host_list.append(host1)
							client_id_list.append(client_id2)
							user_id_list.append(user_id3)
							date_time_list.append(date_time4)
							method_list.append(method5)
							endpoint_list.append(endpoint6)
							protocol_list.append(protocol7)
							response_code_list.append(response_code8)
							content_size_list.append(content_size9)
							user_agents_list.append(user_agents10)
							mobile_list.append(mobile11)
							user_agent_flag_list.append(user_agent_flag)
							section_list.append(section11)

							if((count+1)%5000==0):
								bulk_insert_logs(host_list,client_id_list,user_id_list,
						date_time_list,method_list,endpoint_list,protocol_list,
						response_code_list,content_size_list,user_agents_list,
						mobile_list,user_agent_flag_list,section_list)
								host_list              = []
								client_id_list         = []
								user_id_list           = []
								date_time_list         = []
								method_list            = []
								endpoint_list          = []
								protocol_list          = []
								response_code_list     = []
								content_size_list      = []
								user_agents_list       = []
								mobile_list            = []
								user_agent_flag_list   = []
								section_list           = []
				

					#f.write(line_to_parse)
					count+=1

				left = num_lines%5000
				bulk_insert_logs_2(host_list,client_id_list,user_id_list,
					date_time_list,method_list,endpoint_list,protocol_list,
					response_code_list,content_size_list,user_agents_list,
					mobile_list,user_agent_flag_list,section_list,left)

				print "done"
				f.close()


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
	cursor.execute("SELECT distinct(host), date_time from readlog_logconfig_test  where user_agents like %s group by host",(p))

	data = cursor.fetchall()
	count = 0
	temp = []
	for row in data:
		ip = data[count]
		temp.append(ip)
		count+=1

	print len(temp)
	for i in range(len(temp)):
		cursor.execute("SELECT count(*) from readlog_logconfig_test where host = %s",temp[i][0])
		c1 = cursor.fetchall()
		hits = c1[0][0]
		# print i+1, ": ", hits
		cursor.execute("INSERT INTO readlog_badbotsip_test (host, Description, date_time, hits) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE host = %s, Description = %s, date_time = %s, hits = %s",(str(temp[i][0]), description_bad_ip, temp[i][1], hits,str(temp[i][0]), description_bad_ip, temp[i][1], hits))

	local_host = '127.0.0.1'
	cursor.execute("delete from readlog_badbotsip_test where host = %s",(local_host))
	conn.commit()
	print "Preliminary test done."


def excess_requests_in_recent_past():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	cursor.execute("SELECT distinct(host) from readlog_badbotsip_test")
	data = cursor.fetchall()
	b = set(data)
	x = list(b)
	xx = []
	for i in range(len(x)):
		xx.append(x[i][0])


	cursor.execute("SELECT distinct(host) from readlog_goodbots_test")
	data = cursor.fetchall()
	g = set(data)
	y = list(g)
	yy = []

	for i in range(len(y)):
		yy.append(y[i][0])


	# cursor.execute("SELECT distinct(host) from readlog_goodusers_test")
	# data = cursor.fetchall()
	# u = set(data)
	# z = list(u)
	# zz = []

	# for i in range(len(z)):
	# 	zz.append(z[i][0])
	
	cursor.execute("SELECT host, count(*) as c from readlog_logconfig_test group by host order by c desc limit 2000")
	data = cursor.fetchall()
	t = set(data)
	w = list(t)
	s = []
	
	for i in range(len(w)):
		s.append(w[i][0])

	ff = set(xx)|set(yy)
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
		cursor.execute("SELECT max(date_time) from readlog_logconfig_test_dump where host = %s",(distinct_host_list[i]))
		
		data = cursor.fetchone()
		y = data[0]
		x = str(data[0])
		p = x.split()
		pre = datetime.strptime(p[1],"%H:%M:%S")
		sub = datetime.strptime("01:00","%M:%S")
		dif = pre-sub
		dif = str(dif)
		final = p[0] + 	" " + dif
		
		cursor.execute("SELECT host, count(*) as c from readlog_logconfig_test_dump where host = %s and date_time > %s",(host_ip, final))
		p1 = cursor.fetchall()

		if(p1[0][1]>=20):	
			crumb = host_ip
			suspicious_ip.append(crumb)
			dts_list.append(y)
			cursor.execute("SELECT count(*) from readlog_logconfig_test_dump where host = %s",host_ip)
			hits_data = cursor.fetchall()
			host_ip_count.append(hits_data[0][0])
			# if(crumb == '180.215.181.46'):
			# 	print final, " ", crumb, " ", hits_data[0][0]

	
	print "Suspicious ips: ",len(suspicious_ip)
	for i in range(len(suspicious_ip)):
		cursor.execute("INSERT INTO readlog_suspicious_test (host, Description, date_time, hits) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE host = %s, Description = %s, date_time = %s, hits = %s",(suspicious_ip[i], "Excess access in one minute", dts_list[i], host_ip_count[i],suspicious_ip[i], "Excess access in one minute", dts_list[i], host_ip_count[i]))
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
		cursor.execute("select distinct(host), date_time, count(*) from readlog_logconfig_test where user_agents like %s and host REGEXP %s group by host",(a[i],b[i]))
		data= cursor.fetchall()
		date_list = []
		print a[i]," : ",len(data)
		
		for x  in range(len(data)):
			temp.append(data[x][0])
			date_list.append(data[x][1])
			#hitslist.append(data[x][2])
		
		for i in range(len(temp)):
			cursor.execute("SELECT count(*) from readlog_logconfig_test_dump where host = %s", (temp[i]))
			count_temp = cursor.fetchall()

			cursor.execute("INSERT INTO readlog_goodbots_test (host, Description, date_time, hits) VALUES (%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE host = %s, Description = %s, date_time = %s, hits = %s",(temp[i], desc[count], date_list[i], count_temp[0][0],temp[i], desc[count], date_list[i], count_temp[0][0]))

		count+=1

	conn.commit()
	print "Good bots done"

def scrappers():

	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()


	a1='Offline Explorer|SiteSnagger|WebCopier|WebReaper|WebStripper|WebZIP|TeleportPro|Xaldon_WebSpider'
	a = 'Offline Explorer'	
	
	cursor.execute("select distinct(host), user_agents, date_time from readlog_logconfig_test where user_agents REGEXP %s group by host",(a))
	data= cursor.fetchall()
	
	for i in range(len(data)):
		ips = str(data[i][0])
		scr = str(data[i][1])
		dts = data[i][2]
		des = scr + " Scrapper"


		cursor.execute("SELECT count(*) from readlog_logconfig_test_dump where host = %s",ips)
		c1 = cursor.fetchall()
		hits = c1[0][0]

		cursor.execute("INSERT INTO readlog_badbotsip_test (host, Description, date_time, hits) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE host = %s, Description = %s, date_time = %s, hits = %s",(ips,des,dts, hits,ips,des,dts, hits))

	conn.commit()
	print "Scrappers found"

def badbot_agents():

	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()

	b = ['MJ12bot','ia_archiver|nutch|AhrefsBot','Python-urllib|oBot','UniversalFeedParser|DigExt']
	gg = set()
	for i in range(4):
		cursor.execute("select distinct(host), date_time from readlog_logconfig_test where user_agents REGEXP %s group by host",(b[i]))
		data= cursor.fetchall()
		
		print len(data)
		for x in range(len(data)):
			ips = str(data[x][0])
			scr = b[i]
			dts = data[x][1]
			des = str(scr) + " Bot"

			cursor.execute("SELECT count(*) from readlog_logconfig_test_dump where host = %s",ips)
			c1 = cursor.fetchall()
			hits = c1[0][0]

			cursor.execute("INSERT INTO readlog_badbotsip_test (host, Description, date_time, hits) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE host = %s, Description = %s, date_time = %s, hits = %s",(ips,des,dts,hits,ips,des,dts,hits))

	conn.commit()

def check():
	
	preliminary_test()
	botAndIp()
	scrappers()
	badbot_agents()
	excess_requests_in_recent_past()
	

if __name__ == '__main__':
	start = time.time()
	print start
	#get_old_access_logs()
	check()
	end = time.time()
	print end - start
	
