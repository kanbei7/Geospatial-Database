#!/usr/bin/env python
import xmlrpclib
import sys
import csv
import time
from xmlrpclib import ServerProxy

s = ServerProxy('http://localhost:8200', allow_none = True)
data_from_serv = []

location_rows = []
f = open('test.csv', 'r')
for row in csv.reader(f):
	location_rows.append(row)
f.close()


for l in location_rows:
	data_from_serv = s.new(l[0],l[1],l[2])
	with open('file.txt', 'a') as output:
		json.dump({'userid': data_from_serv[0], 'latitude': data_from_serv[1], 'longitude': data_from_serv[2]}, output, indent=4)

	time.sleep(2)


'''
for i in csv_rows:
	if i[0] == 'PUT':
		s.set(i[1],i[2])
		print "PUT SECCESS"
	elif i[0] == 'GET':
		print s.get(i[1])
	if i[0] == 'REMOVE':
		s.delet(i[1])
'''


