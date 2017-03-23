#!/usr/bin/env python
import xmlrpclib
import sys
import os
import csv
import time
from xmlrpclib import ServerProxy
import json
CLIENT_HOME='./client_data/'
s = ServerProxy('http://localhost:8200', allow_none = True)

#flst=os.listdir(CLIENT_HOME)

flst = list((fn for fn in os.listdir(CLIENT_HOME) if fn.endswith('.csv')))
print (len(flst))
Lines={}
USERS_SET=[]
flst=flst[1:]
for user in flst:
	uid=str(user.split('.')[0])
	USERS_SET.append(uid)
	#print (user)
	f=open(CLIENT_HOME+user,'r')
	Lines[uid]=f.readlines()
	f.close()
	#print Lines[uid][0]
	#print (str(len(Lines[uid])))
#print Lines
for i in range(41):
	for uid in USERS_SET:
		#print uid
		l=Lines[uid][i].strip().split(',')
		s.set(l[0],float(l[1]),float(l[2]))
		#print s.get()	

	with open('Result.json', 'w') as output:
		json.dump(s.get(), output, indent=4)

'''
location_rows = []
f = open('0bf7a39c54b370bdb0ffb1d6b8e4616b.csv', 'r')
for row in csv.reader(f):
	location_rows.append(row)
f.close()

for l in location_rows:
	s.set(l[0],l[1],l[2])
'''	

