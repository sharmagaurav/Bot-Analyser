#!/usr/bin/env python
import os
import subprocess
import re
import MySQLdb
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

class LogParser(object):

	def __init__(self, host, client_id, user_id, date_time,
				 method, endpoint, protocol, response_code,
				 content_size, user_agents, mobile, user_agent_flag):
		self.host            = host #127.0.0.1
		self.client_id       = client_id #hyphen -
		self.user_id         = user_id #second hyphen -
		self.date_time       = date_time	          #Datetime
		self.method          = method #GET, POST
		self.endpoint        = endpoint #admin/login/?next=/admin/
		self.protocol        = protocol #HTTP/1.1
		self.response_code   = response_code #200 status code
		self.content_size    = content_size #1305
		self.user_agents     = user_agents #User agent description
		self.mobile          = mobile #Mobile user present or not
		self.user_agent_flag = user_agent_flag

	def show_data(self):
		print self.host
		print self.client_id
		print self.user_id
		print self.date_time
		print self.method
		print self.endpoint
		print self.protocol
		print self.response_code
		print self.content_size
		print self.user_agents
		print self.mobile

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

def over_write_files():
	f = open('/home/gaurav/myproject/readlog/testlogs.txt','w')
	f.write("")
	f.close()

def bulk_insert_logs_2(host_list,client_id_list,user_id_list,
			date_time_list,method_list,endpoint_list,protocol_list,
			response_code_list,content_size_list,user_agents_list,
			mobile_list,user_agent_flag_list,left):
	
	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()
	try:
		for i in range(left):
			cursor.execute("INSERT INTO readlog_logconfig (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i]))
	except:
		pass
	conn.commit()


def bulk_insert_logs(host_list,client_id_list,user_id_list,
			date_time_list,method_list,endpoint_list,protocol_list,
			response_code_list,content_size_list,user_agents_list,
			mobile_list,user_agent_flag_list):
	
	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()
	try:
		for i in range(5000):
			cursor.execute("INSERT INTO readlog_logconfig (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i]))
	except:
		pass
	conn.commit()


def get_old_access_logs():
	f = open('/home/gaurav/myproject/30_access.log','r')
	old_log_pattern = '^\[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s*" (\d{3}) (\S+) (\S+) (\S+) (.*$)'
	date_res = "([^:]+):(\d+:\d+:\d+) ([^\]]+)"
	count = 0
	text = f.readlines()
	f.close()

	num_lines = sum(1 for line in open('/home/gaurav/myproject/30_access.log','r'))
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


	f = open("/home/gaurav/myproject/readlog/testlogs.txt",'a')
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
		print count+1, m, len(m)
		if matchObj:
			if len(m)==0:
				pass
			else:
				host1          = m[0]
				client_id2     = t
				client_id2 = str(client_id2)
				user_id3       = '-'
				date_time4     = matchObj.group(1)
				method5        = matchObj.group(2)
				endpoint6      = matchObj.group(3)
				protocol7      = matchObj.group(4)
				response_code8 = matchObj.group(5)
				content_size9  = matchObj.group(6)
				user_agents10  = matchObj.group(8) + " " + matchObj.group(9)
				user_agent_string = str(user_agents10)
				
				user_agent_flag = 0
				if(user_agents10):
					user_agent_flag = 1

				if mobile_string in user_agent_string:
					mobile_string_present = 1
				
				mobile11 = mobile_string_present

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

				if((count+1)%5000==0):
					bulk_insert_logs(host_list,client_id_list,user_id_list,
			date_time_list,method_list,endpoint_list,protocol_list,
			response_code_list,content_size_list,user_agents_list,
			mobile_list,user_agent_flag_list)
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
	

		f.write(line_to_parse)
		count+=1

	left = num_lines%5000
	bulk_insert_logs_2(host_list,client_id_list,user_id_list,
		date_time_list,method_list,endpoint_list,protocol_list,
		response_code_list,content_size_list,user_agents_list,
		mobile_list,user_agent_flag_list,left)

	print "done"
	f.close()

if __name__ == '__main__':

	over_write_files()
	get_old_access_logs()