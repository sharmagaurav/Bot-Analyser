#! /usr/bin/env python
import MySQLdb
import re
from datetime import datetime
import time

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



def total_hits_param():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	t=['readlog_badbotsip', 'readlog_goodbots', 'readlog_suspicious']

	length = len(t)
	centroid_total_hits_param = []

	for i in range(length):
		cursor.execute("select avg(hits) from %s " %t[i])
		data= cursor.fetchall()
		centroid_total_hits_param.append(data[0][0])
		#print centroid_total_hits_param[i]

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
			session_time_string = str(session_time)
			t = max_date[i]
			t = datetime.strftime(t, "%Y-%m-%d")
			standard_session_time = t + " 00:30:00"
			session_time_full = t + " " + session_time_string
			standard_session_time = datetime.strptime(standard_session_time, "%Y-%m-%d %H:%M:%S")
			session_time_full = datetime.strptime(session_time_full, "%Y-%m-%d %H:%M:%S")

			if(session_time_full<standard_session_time):
				pt = session_time_full
				total_seconds = pt.second+pt.minute*60+pt.hour*3600
				if(total_seconds==0):
					total_seconds = 1
				sessions_list[i] = 1
				avg_time_per_session[i] = total_seconds
				avg_hits_per_session[i] = host_hits_list[i]
				avg_time_between_two_requests[i] = float(total_seconds)/float(host_hits_list[i])
				#print session_time_full," ", total_seconds, " ", host_hits_list[i], " ", avg_time_between_two_requests[i]
				# centroid_avg_time_between_two_requests_bad = sumss/len(avg_time_between_two_requests)
				# centroid_avg_session_hits_bad = sumhh/len(avg_hits_per_session)
				# centroid_avg_time_per_session_bad = sumtt/len(avg_time_per_session)
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
					# print requests[m]," - ",requests[n]," = ", diff
					# print "Diff ",requests[m], " - ", requests[n], " = " ,diff
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
		


def sessiondiscovery():
	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	a = ['readlog_badbotsip','readlog_goodbots', 'readlog_suspicious']
	sumss = [0.0]*3
	sumh  = [0.0]*3
	for z in range(3):
		cursor.execute("select host,hits from %s " %a[z])
		data = cursor.fetchall()

		bad_hosts_list      = []
		bad_hosts_hits_list = []
		min_date            = []
		max_date            = []

		for i in range(len(data)):
			bad_hosts_list.append(data[i][0])
			bad_hosts_hits_list.append(data[i][1])
			bad = data[i][0]

			cursor.execute("SELECT min(date_time), max(date_time) from readlog_logconfig WHERE host = %s",(bad))
			date_data = cursor.fetchall()
			min_date.append(date_data[0][0])
			max_date.append(date_data[0][1])

		avg_session_time     = [0.0]*len(bad_hosts_list)
		hits_per_session     = [0.0]*len(bad_hosts_list)
		hits_per_session_temp     = []
		time_between_request = [0.0]*len(bad_hosts_list)
		time_request_temp    = []
		time_between_two_requests_in_session = [0.0]*len(bad_hosts_list)

		for i in range (len(bad_hosts_list)):
			time_request_temp    = []
			session_time = max_date[i] - min_date[i]
			session_time_string = str(session_time)
			t = max_date[i]
			t = datetime.strftime(t, "%Y-%m-%d")
			standard_session_time = t + " 00:30:00"
			session_time_full = t + " " + session_time_string
			standard_session_time = datetime.strptime(standard_session_time, "%Y-%m-%d %H:%M:%S")
			session_time_full = datetime.strptime(session_time_full, "%Y-%m-%d %H:%M:%S")
			
			if(session_time_full<standard_session_time):
				pt = session_time_full
				total_seconds = pt.second+pt.minute*60+pt.hour*3600

				if(total_seconds <= 1):
					avg_session_time[i] = 1
					hits_per_session[i] = bad_hosts_hits_list[i]
					time_between_two_requests_in_session[i] = 0
				else:
					avg_session_time[i] = total_seconds
					hits_per_session[i] = bad_hosts_hits_list[i]
					time_between_two_requests_in_session[i] = bad_hosts_hits_list[i]/total_seconds

			else:
				
				cursor.execute("SELECT date_time from readlog_logconfig WHERE host = %s",(bad_hosts_list[i]))
				temp = cursor.fetchall()
				request_list = []
				for x in range(len(temp)):
					request_list.append(temp[x][0])
				high  = request_list[1]
				highs = request_list[1]
				low   = request_list[0]
				lows  = request_list[0]
				count = 0
				access_time = 0
				counter = 1
				session_count = 0
				for x in range(1,len(request_list)-1):
										
					t = datetime.strftime(low,"%Y-%m-%d")
					cc = t+" 00:30:00"
					cc = datetime.strptime(cc,'%Y-%m-%d %H:%M:%S')
					diff = str(high - low)
					dd = t+ " " + diff
					dd = datetime.strptime(dd, '%Y-%m-%d %H:%M:%S')
					agg=0
					if(counter<x):
						for c in range(len(hits_per_session_temp)):
							agg +=hits_per_session_temp[c]

					if(dd < cc):
						count+=1
						temp1 = str(request_list[x] - request_list[x-1])
						temp1 = datetime.strptime(temp1, '%H:%M:%S')
						access_time = temp1.second +  temp1.minute*60 + temp1.hour*3600
						time_request_temp.append(access_time)
						high = request_list[x+1]
						low = request_list[x]
					else:
						session_count+=1
						sums = 0
						for y in range(len(time_request_temp)):
							sums+=time_request_temp[y]
						if(count==0):
							count=1
						hits_per_session_temp.append(count)

						time_between_two_requests_in_session[i] = sums/count
						time_request_temp = []
						count = 0
						highs = request_list[x-1]
						av_st = highs-lows
						high  = request_list[x+1]
						low   = request_list[x]
						lows  = request_list[x+1]
					counter =x
				print z," ", session_count
				if(session_count==0):
					session_count=1
				hits_per_session[i] = bad_hosts_hits_list[i]/session_count
			print "hits per session",hits_per_session[i], "=", bad_hosts_hits_list[i]," / "

		for y in range(len(time_between_two_requests_in_session)):
			sumss[z] += time_between_two_requests_in_session[y]

		global centroid_avg_time_between_two_requests_bad
		global centroid_avg_time_between_two_requests_good
		global centroid_avg_time_between_two_requests_suspicious
		global centroid_avg_session_hits_bad
		global centroid_avg_session_hits_good
		global centroid_avg_session_hits_suspicious
		centroid_avg_time_between_two_requests_bad = sumss[0]
		centroid_avg_time_between_two_requests_good = sumss[1]
		centroid_avg_time_between_two_requests_suspicious = sumss[2]

		for m in range(len(hits_per_session)):
			sumh[z] += hits_per_session[m]
		centroid_avg_session_hits_bad =sumh[0]
		centroid_avg_session_hits_good = sumh[1]
		centroid_avg_session_hits_suspicious = sumh[2]

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

			sum = sum + len(data_count)

		avg = float(sum) / len(host_list)
		#print "X : ",avg

		if(x==0):
			centroid_avg_section_bad = avg
		elif(x==1):
			centroid_avg_section_good = avg
		elif(x==2):
			centroid_avg_section_suspicious = avg
		conn.commit()


if __name__ == '__main__':
	total_hits_param()
	# sessiondiscovery()
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