#! /usr/bin/env python
import MySQLdb
import re
from datetime import datetime
import time
import math
import numpy

host_list      = []
feature1_list  = []
feature2_list  = []
feature3_list  = []
feature4_list  = []
feature5_list  = []

# avg_time_per_session = [0.0]*len(host_list)
# avg_hits_per_session = [0.0]*len(host_list)
# avg_time_between_two_requests = [0.0]*len(host_list)

# coordinate1 = []
# coordinate2 = []
# coordinate3 = []
# coordinate4 = []
# coordinate5 = [] 

t=['readlog_badbotsip', 'readlog_goodbots', 'readlog_suspicious']

def extract_hosts():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	t = 'readlog_logconfig_test'
	cursor.execute("select host, count(*) from %s group by host " %t)
	data= cursor.fetchall()
	l= len(data)
	print l

	for i in range(l):
		host_list.append(data[i][0])

	# print host_list
	conn.commit()


def feature1():
	print "entered feature1"
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	m = len(host_list)
	print m
	
	for i in range(m):	
		cursor.execute("select count(*) from readlog_logconfig_test where host = %s ",(host_list[i]))
		data= cursor.fetchall()
		feature1_list.append(data[0][0])
	
	# print feature1_list
	conn.commit()


def feature2():
	print "entered feature2"
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	m = len(host_list)
		
	for i in range(m):	
		cursor.execute("SELECT count(*) as c, section from readlog_logconfig_test WHERE host = %s group by section having c > 5",(host_list[i]))
		data = cursor.fetchall()
		feature2_list.append(len(data))
	
	l= len(feature2_list)
	print l
	
	conn.commit()


def feature3():
	print "entered feature3"

	avg_time_per_session = [0.0]*len(host_list)
	avg_hits_per_session = [0.0]*len(host_list)
	avg_time_between_two_requests = [0.0]*len(host_list)

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	l = len(host_list)
	print l

	host_hits_list = []
	max_date  = []
	min_date  = []
	
	for i in range(l):
		cursor.execute("select count(*) from readlog_logconfig_test where host = %s group by host", (host_list[i]))
		data = cursor.fetchall()
		host_hits_list.append((data[0][0]))

		cursor.execute("select min(date_time), max(date_time) from readlog_logconfig_test where host = %s",(host_list[i]))
		date_data = cursor.fetchall()
		min_date.append(date_data[0][0])
		max_date.append(date_data[0][1])


	for i in range(len(host_list)):

		# global avg_time_per_session
		# global avg_hits_per_session
		# global avg_time_between_two_requests 

		sessions_list = [0]*len(host_list)
		session_time = max_date[i] - min_date[i]
		s = session_time.seconds

		if(s<1800):
			total_seconds = s
			if(total_seconds==0):
				total_seconds = 1
			sessions_list[i] = 1
			avg_time_per_session[i] = total_seconds
			avg_hits_per_session[i] = host_hits_list[i]
			avg_time_between_two_requests[i] = float(total_seconds)/float(host_hits_list[i])

		else:
	
			requests = []
			time_between_request_in_one_session = []
			time_between_requests = []
			cursor.execute("SELECT date_time from readlog_logconfig_test WHERE host = %s order by date_time asc", (host_list[i]))
			date_data = cursor.fetchall()

			for y in range(len(date_data)):
				requests.append(date_data[y][0])

			m = 1
			low  = requests[0]
			high = requests[1]
			time_per_session = []
			for n in range(len(requests)-1):
				diff = requests[n]-requests[m]
				
				try:
					diff = datetime.strptime(str(diff), '%H:%M:%S')
				except:
					continue
				st_time = datetime.strptime("00:30:00", '%H:%M:%S')
				if(diff<st_time):
					tot_seconds = diff.second+diff.minute*60+diff.hour*3600
					time_between_request_in_one_session.append(tot_seconds)
					high = requests[n]
					m+=1
				else:
					ps = high-low
					session_length = ps.second+ps.minute*60+ps.hour*3600
					time_per_session.append(session_length)
					low = requests[n+1]
					ss = 0
					sessions_list[i]+=1
					for b in range(len(time_between_request_in_one_session)):
						ss += time_between_request_in_one_session[b]
					length = len(time_between_request_in_one_session)
					if(length==0):
						length=1
					time_between_requests.append(ss/length)
					time_between_request_in_one_session = []
					m+=2
					n+=2
					
			add = 0
			for n in range(len(time_per_session)):
				add+=time_per_session[n]

			ls = len(time_per_session)
			if(ls==0):
				ls=1
			avg_time_per_session[i] = add/ls

			add = 0
			for n in range(len(time_between_requests)):
				add += time_between_requests[n]
			ls = len(time_between_requests)
			if(ls==0):
				ls=1
			avg_time_between_two_requests[i] = add/ls

	print len(avg_time_per_session)
	print len(avg_hits_per_session)
	print len(avg_time_between_two_requests)

	global feature3_list
	global feature4_list
	global feature5_list

	feature3_list = list(avg_time_per_session)
	feature4_list = list(avg_hits_per_session)
	feature5_list = list(avg_time_between_two_requests)

	print len(feature3_list)
	print len(feature4_list)
	print len(feature5_list)


	conn.commit()



def insert_db():

	print "entered db"
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	l=len(host_list)

	for i in range(l):

		# RUN THIS COMMNTD QUERY WHEN BAAKI TEENO LIST ARE COMPLETE. TRUNCATE TABLE SIDE BY SIDE
		cursor.execute("INSERT INTO readlog_feature_vector (host,no_of_requests,no_of_sections,avg_session_time,hits_per_session,time_bw_requests) VALUES (%s,%s,%s,%s,%s,%s)", (host_list[i],feature1_list[i],feature2_list[i],feature3_list[i],feature4_list[i],feature5_list[i]))	
		# cursor.execute("INSERT INTO readlog_feature_vector (host,no_of_requests,no_of_sections) VALUES (%s,%s,%s)", (host_list[i],feature1_list[i],feature2_list[i]))	
	
	conn.commit()


def cal_distance():
	print "entered cal_distance"
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
		
	m = len(host_list)
	print m

	centroid1 =[11,32,61]
	centroid2 =[5,70,20]
	centroid3 =[60,10,90]
	centroid4 =[11,32,61]
	centroid5 =[36,15,40]

	dist = [0]*3
	
	for i in range(100):
		
		for j in range(3):
			
			# print feature1_list[i], feature2_list[i] #, feature3_list[i], feature4_list[i], feature5_list[i]
			a = numpy.array((centroid1[j],centroid2[j],centroid3[j],centroid4[j],centroid5[j]))
			b = numpy.array((feature1_list[i], feature2_list[i], feature3_list[i], feature4_list[i], feature5_list[i]))
			dist[j] = numpy.linalg.norm(a-b)
			print "distance of",i, "of table", j ,"is", dist[j]
			
		# a = min(dist[0],dist[1])
		# print a

		arr = numpy.array([dist[0],dist[1],dist[2]])    
		min_index = numpy.argmin(arr)
		# cursor.execute("INSERT INTO t[min_index] (host,) VALUES (%s,%s,%s,%s,%s,%s)", (host_list[i],feature1_list[i],feature2_list[i],feature3_list[i],feature4_list[i],feature5_list[i]))	




	conn.commit()	
 

if __name__ == '__main__':

	extract_hosts()
	feature1()
	feature2()
	feature3()
	# insert_db()
	cal_distance()