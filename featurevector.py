import MySQLdb
import re
from datetime import datetime
import time

host_list      = []
feature1_list  = []
feature2_list  = []
feature3_list  = []
feature4_list  = []
feature5_list  = []

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
		# print data[0][0]
		feature1_list.append(data[0][0])
	
	# l= len(feature1_list)
	# print l
	print feature1_list
	conn.commit()


def feature2():
	print "entered feature2"
	conn = MySQLdb.connect(host = "localhost", user = "root",
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

insert_db():

	conn = MySQLdb.connect(host = "localhost", user = "root",
                            passwd = "1234", db = "logparsers")
	cursor = conn.cursor()


	
	conn.commit()

 

if __name__ == '__main__':

	extract_hosts()
	feature1()
	feature2()
	insert_db()