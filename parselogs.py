#!/usr/bin/env python
import os
import subprocess
import re
import MySQLdb
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

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


def bulk_insert_logs_2(host_list,client_id_list,user_id_list,
			date_time_list,method_list,endpoint_list,protocol_list,
			response_code_list,content_size_list,user_agents_list,
			mobile_list,user_agent_flag_list,section_list,left):
	
	conn = MySQLdb.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()
	try:
		for i in range(left):
			cursor.execute("INSERT INTO readlog_logconfig (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i], section_list[i]))
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
			cursor.execute("INSERT INTO readlog_logconfig (host,client_id,user_id,date_time,method,endpoint,protocol,response_code,content_size,user_agents,mobile,user_agents_flag,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (host_list[i],client_id_list[i],user_id_list[i],date_time_list[i],method_list[i],endpoint_list[i],protocol_list[i], response_code_list[i], content_size_list[i], user_agents_list[i], mobile_list[i], user_agent_flag_list[i], section_list[i]))
	except:
		pass
	conn.commit()


def get_old_access_logs():
	old_log_pattern = '^\[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s*" (\d{3}) (\S+) (\S+) (\S+) (.*$)'
	date_res = "([^:]+):(\d+:\d+:\d+) ([^\]]+)"

	path = r'access-logs'
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

if __name__ == '__main__':

	get_old_access_logs()