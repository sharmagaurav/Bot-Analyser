from math import log
import MySQLdb
import re
from datetime import datetime
import time

def parameter1():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	t=['readlog_badbotsip', 'readlog_goodbots', 'readlog_suspicious']


	# t[0] = 'readlog_badbotsip'
	length = len(t)
	centroid1 = []

	for i in range(length):

		cursor.execute("select avg(hits) from %s " %t[i])
    	
		data= cursor.fetchall()
		# print data[0][0]
		centroid1.append(data[0][0])
		print centroid1[i]

	
	conn.commit()



def parameter2():

	pass

def sessiondiscovery():
	
	# ip= '23.212.50.38' 

	# ipdata = list(log.track_ip(ip))
	# initial_dt = ipdata[0]['date_time']
	# sess = [x for x in ipdata if x['date_time'] < initial_dt + date_time.timedelta(0,60)]

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()

	t=['readlog_badbotsip', 'readlog_goodbots', 'readlog_suspicious']


	# t[0] = 'readlog_badbotsip'
	length = len(t)
	centroid1 = []

	for i in range(length):

		cursor.execute("select avg(hits) from %s " %t[i])
    	
		data= cursor.fetchall()
		# print data[0][0]
		centroid1.append(data[0][0])
		print centroid1[i]

	
	conn.commit()








    
    

if __name__ == '__main__':
	# parameter1()

	parameter2()
	sessiondiscovery()