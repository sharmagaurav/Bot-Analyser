#! /usr/bin/env python
import MySQLdb
import re
from datetime import datetime
import time
import numpy
import math

# First centroid : Total hits
centroid_total_hits_bad = None
centroid_total_hits_good = None
centroid_total_hits_suspicious = None
# Second centroid : Average number of section accessed
centroid_avg_section_bad = None
centroid_avg_section_good = None
centroid_avg_section_suspicious = None
#Third : Average time per session
centroid_avg_time_per_session_bad = None
centroid_avg_time_per_session_good = None
centroid_avg_time_per_session_suspicious = None
#Fourth : Average session hits
centroid_avg_session_hits_bad = None
centroid_avg_session_hits_good = None
centroid_avg_session_hits_suspicious = None
#Fifth : Average time between two consecutive requests
centroid_avg_time_between_two_requests_bad = None
centroid_avg_time_between_two_requests_good = None
centroid_avg_time_between_two_requests_suspicious = None

total_hits_param_bad        = []
total_hits_param_good       = []
total_hits_param_suspicious = []
total_hits_param_good_user  = []

avg_time_per_session_bad        = []
avg_time_per_session_good       = []
avg_time_per_session_suspicious = []
avg_time_per_session_good_user  = []

avg_hits_per_session_bad        = []
avg_hits_per_session_good       = []
avg_hits_per_session_suspicious = []
avg_hits_per_session_good_user  = []

avg_time_between_two_requests_bad        = []
avg_time_between_two_requests_good       = []
avg_time_between_two_requests_suspicious = []
avg_time_between_two_requests_good_user  = []

avg_section_hits_bad        = []
avg_section_hits_good       = []
avg_section_hits_suspicious = []
avg_section_hits_good_user  = []

def total_hits_param():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	t=['readlog_badbotsip', 'readlog_goodbots', 'readlog_suspicious']

	length = len(t)
	centroid_total_hits_param = []

	for i in range(length):
		cursor.execute("SELECT hits from %s " %t[i])
		data_hits = cursor.fetchall()
		if(i==0):
			for k in range(len(data_hits)):
				total_hits_param_bad.append(data_hits[k][0])
		if(i==1):
			for k in range(len(data_hits)):
				total_hits_param_good.append(data_hits[k][0])
		if(i==2):
			for k in range(len(data_hits)):
				total_hits_param_suspicious.append(data_hits[k][0])

	for i in range(length):
		cursor.execute("select avg(hits) from %s " %t[i])
		data= cursor.fetchall()
		centroid_total_hits_param.append(data[0][0])

	global centroid_total_hits_bad
	global centroid_total_hits_good
	global centroid_total_hits_suspicious
	centroid_total_hits_bad = centroid_total_hits_param[0]
	centroid_total_hits_good = centroid_total_hits_param[1]
	centroid_total_hits_suspicious = centroid_total_hits_param[2]
	
	conn.commit()


def session_dis():
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	li = ['readlog_badbotsip','readlog_goodbots', 'readlog_suspicious']

	for z in range(3):
		host_list = []
		host_hits_list = []
		max_date  = []
		min_date  = []
		

		cursor.execute("select host,hits from %s" %li[z])
		data = cursor.fetchall()

		for i in range(len(data)):
			host_list.append(data[i][0])
			host_hits_list.append((data[i][1]))
			bad = data[i][0]

			cursor.execute("select min(date_time), max(date_time) from readlog_logconfig where host = %s",(bad))
			date_data = cursor.fetchall()
			min_date.append(date_data[0][0])
			max_date.append(date_data[0][1])

		avg_time_per_session = [0.0]*len(host_list)
		avg_hits_per_session = [0.0]*len(host_list)
		avg_time_between_two_requests = [0.0]*len(host_list)

		global centroid_avg_time_between_two_requests_bad
		global centroid_avg_time_between_two_requests_good
		global centroid_avg_time_between_two_requests_suspicious
		global centroid_avg_session_hits_bad
		global centroid_avg_session_hits_good
		global centroid_avg_session_hits_suspicious
		global centroid_avg_time_per_session_bad
		global centroid_avg_time_per_session_good
		global centroid_avg_time_per_session_suspicious
		sumss = 0.0
		sumhh = 0.0
		sumtt = 0.0

		for i in range(len(host_list)):
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
				cursor.execute("SELECT date_time from readlog_logconfig WHERE host = %s order by date_time asc", (host_list[i]))
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
			total_hits = host_hits_list[i]
			total_sessions = sessions_list[i]
			if(total_sessions==0):
				total_sessions=1
			avg_hits_per_session[i] = float(total_hits)/float(total_sessions)
					

		for i in range(len(avg_time_between_two_requests)):
			sumss+= avg_time_between_two_requests[i]
			sumhh+= avg_hits_per_session[i]
			sumtt+= avg_time_per_session[i]

		if(z==0):
			centroid_avg_time_between_two_requests_bad = sumss/len(avg_time_between_two_requests)
			centroid_avg_session_hits_bad = sumhh/len(avg_hits_per_session)
			centroid_avg_time_per_session_bad = sumtt/len(avg_time_per_session)
		elif(z==1):
			centroid_avg_time_between_two_requests_good = sumss/len(avg_time_between_two_requests)
			centroid_avg_session_hits_good = sumhh/len(avg_hits_per_session)
			centroid_avg_time_per_session_good = sumtt/len(avg_time_per_session)
		elif(z==2):
			centroid_avg_time_between_two_requests_suspicious = sumss/len(avg_time_between_two_requests)
			centroid_avg_session_hits_suspicious = sumhh/len(avg_hits_per_session)
			centroid_avg_time_per_session_suspicious = sumtt/len(avg_time_per_session)
		

		if(z==0):
			for d in range(len(avg_time_per_session)):
				avg_time_per_session_bad.append(avg_time_per_session[d])
			for d in range(len(avg_hits_per_session)):
				avg_hits_per_session_bad.append(avg_hits_per_session[d])
			for d in range(len(avg_time_between_two_requests)):
				avg_time_between_two_requests_bad.append(avg_time_between_two_requests[d])

			aa=0.0
			for k in range(len(avg_hits_per_session_bad)):
				aa += avg_hits_per_session_bad[k]
			print "Compare result : ",aa/len(avg_hits_per_session_bad)

		elif(z==1):
			for d in range(len(avg_time_per_session)):
				avg_time_per_session_good.append(avg_time_per_session[d])
			for d in range(len(avg_hits_per_session)):
				avg_hits_per_session_good.append(avg_hits_per_session[d])
			for d in range(len(avg_time_between_two_requests)):
				avg_time_between_two_requests_good.append(avg_time_between_two_requests[d])
		elif(z==2):
			for d in range(len(avg_time_per_session)):
				avg_time_per_session_suspicious.append(avg_time_per_session[d])
			for d in range(len(avg_hits_per_session)):
				avg_hits_per_session_suspicious.append(avg_hits_per_session[d])
			for d in range(len(avg_time_between_two_requests)):
				avg_time_between_two_requests_suspicious.append(avg_time_between_two_requests[d])

	conn.commit()


def avg_section_hits():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	t = ['readlog_badbotsip','readlog_goodbots','readlog_suspicious']
	global centroid_avg_section_bad
	global centroid_avg_section_good
	global centroid_avg_section_suspicious
	#t = 'readlog_suspicious'
	for x in range(len(t)):
		cursor.execute("select host from %s" %t[x])
		centroid2 = []
		host_list = []
		data= cursor.fetchall()
		sum=0

		for i in range(len(data)):
			host_list.append(data[i][0])

			b = host_list[i]

			cursor.execute("SELECT count(*) as c, section from readlog_logconfig WHERE host = %s group by section having c > 5",(b))
			data_count = cursor.fetchall()

			if(x==0):
				avg_section_hits_bad.append(len(data_count))
			elif(x==1):
				avg_section_hits_good.append(len(data_count))
			elif(x==2):
				avg_section_hits_suspicious.append(len(data_count))

			sum = sum + len(data_count)

		avg = float(sum) / len(host_list)

		if(x==0):
			centroid_avg_section_bad = avg
		elif(x==1):
			centroid_avg_section_good = avg
		elif(x==2):
			centroid_avg_section_suspicious = avg
		conn.commit()

def deviation():
	dev_total_hits_bad        = 0
	dev_total_hits_good       = 0
	dev_total_hits_suspicious = 0

	dev_avg_section_bad        = 0
	dev_avg_section_good       = 0
	dev_avg_section_suspicious = 0

	dev_avg_time_between_two_requests_bad        = 0
	dev_avg_time_between_two_requests_good       = 0
	dev_avg_time_between_two_requests_suspicious = 0

	dev_avg_session_hits_bad        = 0
	dev_avg_session_hits_good       = 0
	dev_avg_session_hits_suspicious = 0

	dev_avg_time_per_session_bad         = 0
	dev_avg_time_per_session_good        = 0
	dev_avg_time_per_session_suspiicious = 0

	#First centroid : Total hits 
	global centroid_total_hits_bad
	global centroid_total_hits_good
	global centroid_total_hits_suspicious
	# Second centroid : Average number of section accessed
	global centroid_avg_section_bad
	global centroid_avg_section_good
	global centroid_avg_section_suspicious
	#Third : Average time per session
	global centroid_avg_time_per_session_bad
	global centroid_avg_time_per_session_good
	global centroid_avg_time_per_session_suspicious
	#Fourth : Average session hits
	global centroid_avg_session_hits_bad
	global centroid_avg_session_hits_good
	global centroid_avg_session_hits_suspicious
	#Fifth : Average time between two consecutive requests
	global centroid_avg_time_between_two_requests_bad
	global centroid_avg_time_between_two_requests_good
	global centroid_avg_time_between_two_requests_suspicious

	# total_hits_param_bad        = []
	# total_hits_param_good       = []
	# total_hits_param_suspicious = []
	# total_hits_param_good_user  = []

	# avg_time_per_session_bad        = []
	# avg_time_per_session_good       = []
	# avg_time_per_session_suspicious = []
	# avg_time_per_session_good_user  = []

	# avg_hits_per_session_bad        = []
	# avg_hits_per_session_good       = []
	# avg_hits_per_session_suspicious = []
	# avg_hits_per_session_good_user  = []

	# avg_time_between_two_requests_bad        = []
	# avg_time_between_two_requests_good       = []
	# avg_time_between_two_requests_suspicious = []
	# avg_time_between_two_requests_good_user  = []

	# avg_section_hits_bad        = []
	# avg_section_hits_good       = []
	# avg_section_hits_suspicious = []
	# avg_section_hits_good_user  = []


	dist = []
	a = numpy.array((float(centroid_avg_section_bad),float(centroid_avg_time_between_two_requests_bad)))
	print a
	for i in range(len(total_hits_param_bad)):
		b = numpy.array((avg_section_hits_bad[i],avg_time_between_two_requests_bad[i]))
		dist.append(numpy.linalg.norm(a-b))

	sum = 0
	for j in range(len(dist)):
		sum+=dist[j]
	dev = sum/len(dist)
	print "deviation bad: ",dev

	dist = []
	a = numpy.array((float(centroid_avg_section_good),float(centroid_avg_time_between_two_requests_good)))
	print a
	for i in range(len(total_hits_param_good)):
		b = numpy.array((avg_section_hits_good[i],avg_time_between_two_requests_good[i]))
		dist.append(numpy.linalg.norm(a-b))

	sum = 0
	for j in range(len(dist)):
		sum+=dist[j]
	dev = sum/len(dist)
	print "deviation good: ",dev

	dist = []
	a = numpy.array((float(centroid_avg_section_suspicious)))
	print a
	for i in range(len(total_hits_param_suspicious)):
		b = numpy.array((avg_section_hits_suspicious[i]))
		dist.append(numpy.linalg.norm(a-b))

	sum = 0
	for j in range(len(dist)):
		sum+=dist[j]
	dev = sum/len(dist)
	print "deviation suspicious: ",dev





if __name__ == '__main__':
	total_hits_param()
	avg_section_hits()
	session_dis()
	print "TOTAL HITS"
	print centroid_total_hits_bad
	print centroid_total_hits_good
	print centroid_total_hits_suspicious
	print "AVERAGE NUMBER OF SECTIONS ACCESSED WHERE HITS GREATER THAN 5"
	print centroid_avg_section_bad
	print centroid_avg_section_good
	print centroid_avg_section_suspicious
	print "AVERAGE TIME BETWEEN TWO REQUESTS"
	print centroid_avg_time_between_two_requests_bad
	print centroid_avg_time_between_two_requests_good
	print centroid_avg_time_between_two_requests_suspicious
	print "AVERAGE HITS PER SESSION"
	print centroid_avg_session_hits_bad
	print centroid_avg_session_hits_good
	print centroid_avg_session_hits_suspicious
	print "AVERAGE TIME PER SESSION"
	print centroid_avg_time_per_session_bad
	print centroid_avg_time_per_session_good
	print centroid_avg_time_per_session_suspicious
	deviation()