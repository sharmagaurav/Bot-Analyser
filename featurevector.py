#! /usr/bin/env python
import pymysql
import pymysql.cursors
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
avg_sessions_per_day = []

test_bad = []
test_good = []
test_suspicious = []

featur1_bad = []
featur2_bad = []
featur3_bad = []

featur1_good = []
featur2_good = []
featur3_good = []

featur1_suspicious = []
featur2_suspicious = []
featur3_suspicious = []

centroid1 =[]
centroid2 =[]
centroid3 =[]

new_centroid1 = []
new_centroid2 = []
new_centroid3 = []


count         = []
# centroid1     = []
# centroid2     = []
# centroid3     = []
deviation     = []
mean_distance = []

sum_mean_distance = [0] * 3
new_mean_distance =[]

t=['readlog_badbotsip', 'readlog_goodbots', 'readlog_suspicious']

def extract_hosts():

	conn = pymysql.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	global host_list

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


	cursor.execute("SELECT distinct(host) from readlog_suspicious_test")
	data = cursor.fetchall()
	u = set(data)
	z = list(u)
	zz = []

	for i in range(len(z)):
		zz.append(z[i][0])
	
	cursor.execute("SELECT host from readlog_logconfig_test group by host")
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

	host_list = list(ffff)
	#print distinct_host_list[0]
	print "Distinct hosts : ",len(host_list)

	conn.commit()


def get_training_centroids():
	conn = pymysql.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor        = conn.cursor()

	des = ['Bad Bots','Good Bots','Suspicious IPs']
	for i in range(len(des)):
		cursor.execute("SELECT count,centroid1, centroid2, centroid3, deviation, distance from readlog_training_centroids where description = %s", (des[i]))
		data = cursor.fetchall()
		#print data[0][0], data[0][1], data[0][2]
		print data
		count.append(data[0][0])
		centroid1.append(data[0][1])
		centroid2.append(data[0][2])
		centroid3.append(data[0][3])
		dev = data[0][4]
		#dev = dev*pow(10,13)
		deviation.append(dev)
		mean_distance.append(data[0][5])

	for i in range(len(des)):
		print des[i]
		print count[i]
		print centroid1[i]
		print centroid2[i]
		print centroid3[i]
		print deviation[i]
		print mean_distance[i]

	conn.commit()
	print "ajkja",len(host_list)

	# count.append(10)
	# count.append(20)
	# count.append(30)

	# deviation.append(1)
	# deviation.append(2)
	# deviation.append(3)

	# mean_distance.append(10)
	# mean_distance.append(11)
	# mean_distance.append(8)



def feature2():
	print "entered feature2"
	conn = pymysql.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	m = len(host_list)
	print m
		
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

	conn = pymysql.connect(host = "localhost", user = "root",
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


	global feature3_list
	global feature4_list
	global feature5_list

	# feature3_list = list(avg_time_per_session)
	# feature4_list = list(avg_hits_per_session)
	feature5_list = list(avg_time_between_two_requests)

	# print len(feature3_list)
	# print len(feature4_list)
	print len(feature5_list)

	conn.commit()


def feature6():
	conn = pymysql.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")

	cursor = conn.cursor()
	
	t = ['readlog_logconfig_test']
	cursor.execute("SELECT distinct(host), count(*) as c from readlog_logconfig_test group by host")
	data = cursor.fetchall()

	hosts = []
	hits = []
	for i in range(len(data)):
		hosts.append(data[i][0])
		hits.append(data[i][1])

	session = [0]*len(data)
	avg_session_hits = [0]*len(data)

	for i in range(len(hosts)):
		cursor.execute("SELECT date_time from readlog_logconfig_test where host = %s order by date_time", (hosts[i]))
		temp = cursor.fetchall()
		dates = []
		#print hosts[i]
		for n in range(len(temp)):
			dates.append(temp[n][0])
		
		j=0
		
		sess_count = 1
		for k in range(1, len(dates)):
			diff = dates[k] - dates[j]
			j+=1
			#print diff
			#print hosts[i]," Diff ", diff," ", type(diff)
			if(diff.days!=0):
				sess_count+=1
				continue
			else:
				if(diff.seconds<1800):
					pass
				else:
					sess_count+=1
		
		cursor.execute("SELECT count(distinct(date(date_time))) from readlog_logconfig_test where host = %s",(hosts[i]))
		data_dates = cursor.fetchall()
		num_dates = data_dates[0][0]	
		session[i] = sess_count
		session[i] = float(session[i])/float(num_dates)

	# for m in range(len(session)):
	# 	avg_session_hits[m] = hits[m]/session[m]
	# sum=0
	# for k in range(len(avg_session_hits)):
	# 	sum+=avg_session_hits[k]
	sums=0.0
	for k in range(len(session)):
		sums+=session[k]
		avg_sessions_per_day.append(session[k])


def insert_db():

	print "entered db"
	conn = pymysql.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	l=len(host_list)

	print l

	for i in range(l):	
		cursor.execute("INSERT INTO readlog_feature_vector (host,no_of_sections,time_bw_requests,sessions_per_day) VALUES (%s,%s,%s,%s)", (host_list[i],feature2_list[i],feature5_list[i],avg_sessions_per_day[i]))	
		
	conn.commit()


def cal_distance():
	print "entered cal_distance"
		
	m = len(host_list)
	print m

	# deviation = [4,2,1]
	# mean_distance  = [11.88,14,9.9]

	countb=0
	cg=0
	cs=0
	dist = [0]*3
	
	global test_bad
	global test_good
	global test_suspicious
	global sum_mean_distance

	for i in range(m):
		
		for j in range(3):			
			# print feature1_list[i], feature2_list[i] #, feature3_list[i], feature4_list[i], feature5_list[i]
			a = numpy.array((centroid1[j],centroid2[j],centroid3[j]))
			b = numpy.array((feature5_list[i], feature2_list[i], avg_sessions_per_day[i]))
			dist[j] = numpy.linalg.norm(a-b)
			# print "distance of",i, "of table", j ,"is", dist[j]
	
		arr = min([dist[0],dist[1],dist[2]])   
		# print arr 
		if(arr == dist[0]):
			if(abs(dist[0] - mean_distance[0])< deviation[0]):
				countb= countb+1
				test_bad.append(host_list[i])
				sum_mean_distance[0] += dist[0]

		elif(arr == dist[1]):
			if(abs(dist[1] - mean_distance[1]) < deviation[1]):
				cg=cg+1
				test_good.append(host_list[i])
				sum_mean_distance[1] += dist[1]

		else:
			if(abs(dist[2] - mean_distance[2])< deviation[2]):
				cs= cs+1
				test_suspicious.append(host_list[i])
				sum_mean_distance[2] += dist[2]

	print "bad" , countb, " ", len(test_bad)
	print test_bad
	print "good" , cg, " ", len(test_good)
	print test_good
	print "sus" , cs, " ", len(test_suspicious)
	print test_suspicious

		
def insert_test():

	conn = pymysql.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	for i in range(len(test_bad)):
		cursor.execute("select count(*), date_time from readlog_logconfig_test where host = %s", test_bad[i])
		data = cursor.fetchall()
		hits = data[0][0]
		datime = data[0][1]
		des = "Bad signature learnt"

		cursor.execute("insert into readlog_badbotsip_test(host,date_time,hits,Description) values (%s,%s,%s,%s)", (test_bad[i],datime,hits,des))


	for i in range(len(test_good)):
		cursor.execute("select count(*), date_time from readlog_logconfig_test where host = %s", test_good[i])
		data = cursor.fetchall()
		hits = data[0][0]
		datime = data[0][1]
		des = "Good signature learnt"

		cursor.execute("insert into readlog_goodbots_test(host,date_time,hits,Description) values (%s,%s,%s,%s)", (test_good[i],datime,hits,des))


	for i in range(len(test_suspicious)):
		cursor.execute("select count(*), date_time from readlog_logconfig_test where host = %s", test_suspicious[i])
		data = cursor.fetchall()
		hits = data[0][0]
		datime = data[0][1]
		des = "Suspicious signature learnt"

		cursor.execute("insert into readlog_suspicious_test(host,date_time,hits,Description) values (%s,%s,%s,%s)", (test_suspicious[i],datime,hits,des))

	conn.commit()


def cal_centroid():

	conn = pymysql.connect(host = "localhost", user = "root",
							passwd = "1234", db = "logparsers")
	cursor = conn.cursor()
	# count = [10,20,30]

	print "count values ", count[0],count[1],count[2]

	sum1_bad = 0.0
	sum2_bad = 0.0
	sum3_bad = 0.0 

	sum1_good = 0.0
	sum2_good = 0.0
	sum3_good = 0.0

	sum1_suspicious = 0.0
	sum2_suspicious = 0.0
	sum3_suspicious = 0.0

	for i in range(len(test_bad)):

		cursor.execute("select no_of_sections, time_bw_requests, sessions_per_day from readlog_feature_vector where host = %s", test_bad[i])
		data2 = cursor.fetchall()

		featur1_bad.append(data2[0][0])
		featur2_bad.append(data2[0][1])
		featur3_bad.append(data2[0][2])

		sum1_bad += data2[0][0]
		sum2_bad += data2[0][1]
		sum3_bad += data2[0][2]
		
	denominator = count[0] + len(test_bad)

	numerator1   = (centroid1[0] * count[0]) + (sum1_bad)
	new_centroid1.append(numerator1/denominator)

	numerator2   = (centroid2[0] * count[0]) + (sum2_bad)
	new_centroid2.append(numerator2/denominator)

	numerator3   = (centroid3[0] * count[0]) + (sum3_bad)
	new_centroid3.append(numerator3/denominator)

	numerator_dist = (mean_distance[0] * count[0]) + sum_mean_distance[0]
	new_mean_distance.append(numerator_dist/denominator)
	
	print "new centroids bad", new_centroid1[0] , new_centroid2[0], new_centroid3[0]
	count[0] = denominator


	for i in range(len(test_good)):

		cursor.execute("select no_of_sections, time_bw_requests, sessions_per_day from readlog_feature_vector where host = %s", test_good[i])
		data2 = cursor.fetchall()
		
		featur1_good.append(data2[0][0])
		featur2_good.append(data2[0][1])
		featur3_good.append(data2[0][2])

		sum1_good += data2[0][0]
		sum2_good += data2[0][1]
		sum3_good += data2[0][2]
		
	denominator = count[1] + len(test_good)

	numerator1   = (centroid1[1] * count[1]) + (sum1_good)
	new_centroid1.append(numerator1/denominator)

	numerator2   = (centroid2[1] * count[1]) + (sum2_good)
	new_centroid2.append(numerator2/denominator)

	numerator3   = (centroid3[1] * count[1]) + (sum3_good)
	new_centroid3.append(numerator3/denominator)

	numerator_dist = (mean_distance[1] * count[1]) + sum_mean_distance[1]
	new_mean_distance.append(numerator_dist/denominator)


	print "new centroids good" , new_centroid1[1] , new_centroid2[1], new_centroid3[1]
	count[1] = denominator


	for i in range(len(test_suspicious)):

		cursor.execute("select no_of_sections, time_bw_requests, sessions_per_day from readlog_feature_vector where host = %s", test_suspicious[i])
		data2 = cursor.fetchall()
	
		featur1_suspicious.append(data2[0][0])
		featur2_suspicious.append(data2[0][1])
		featur3_suspicious.append(data2[0][2])

		sum1_suspicious += data2[0][0]
		sum2_suspicious += data2[0][1]
		sum3_suspicious += data2[0][2]
	
	denominator = count[2] + len(test_suspicious)

	numerator1   = (centroid1[2] * count[2]) + (sum1_suspicious)
	new_centroid1.append(numerator1/denominator)

	numerator2   = (centroid2[2] * count[2]) + (sum2_suspicious)
	new_centroid2.append(numerator2/denominator)

	numerator3   = (centroid3[2] * count[2]) + (sum3_suspicious)
	new_centroid3.append(numerator3/denominator)

	numerator_dist = (mean_distance[2] * count[2]) + sum_mean_distance[2]
	new_mean_distance.append(numerator_dist/denominator)
	

	print "new centroids suspcs" , new_centroid1[2] , new_centroid2[2], new_centroid3[2]
	count[2] = denominator

	print "new counts",count[0],count[1],count[2]
	print "new mean_distance" , new_mean_distance[0], new_mean_distance[1], new_mean_distance[2]

	for i in range(3):	
		cursor.execute("UPDATE readlog_training_centroids set count = %s,centroid1 = %s, centroid2 = %s, centroid3 = %s, distance = %s where id = %s", (count[i],new_centroid1[i],new_centroid2[i],new_centroid3[i],new_mean_distance[i],i+1))	
		
 	conn.commit()

def insert_new_values():

	print "entered insrt insert_new_values"
	conn = pymysql.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	for i in range(3):	
		cursor.execute("UPDATE readlog_training_centroids set count = %s,centroid1 = %s, centroid2 = %s, centroid3 = %s, distance = %s)" %(count[i],new_centroid1[i],new_centroid2[i],new_centroid3[i],new_mean_distance[i]))	
		
	conn.commit()

def lll():
	conn = pymysql.connect(host = "localhost", user = "root",
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


	cursor.execute("SELECT distinct(host) from readlog_suspicious_test")
	data = cursor.fetchall()
	u = set(data)
	z = list(u)
	zz = []

	for i in range(len(z)):
		zz.append(z[i][0])
	
	cursor.execute("SELECT host from readlog_logconfig_test group by host")
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

	host_list = list(ffff)
	#print distinct_host_list[0]
	print "Distinct hosts : ",len(host_list)

if __name__ == '__main__':

	extract_hosts()
	get_training_centroids()
	feature2()
	feature3()
	feature6()
	insert_db()
	cal_distance()
	insert_test()
	cal_centroid()
	insert_new`_values()
	#lll()