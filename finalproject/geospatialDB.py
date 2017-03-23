import os
import sys
import socket
import time
import threading
import pickledb as pk
import datetime
import json

def getTimestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def getKey(x,y):
	return str((int(x),int(y)))

def haskey(key,db):
	if str(key) in set(db.getall()):
		return True
	else:
		return False

DB_MUTEX=threading.Lock()
LOG_MUTEX=threading.Lock()

'''
	def get_long_index(self, n):
		return 1.0*(n-self.LONG_MIN)/self.LONG_RANGE

	def get_lat_index(self, n):
		return 1.0*(n-self.LAT_MIN)/self.LAT_RANGE

	def index2long(self,i):
		return (1.0*i/self.MAXGRID_X+0.5)*self.LONG_RANGE+self.LONG_MIN

	def index2lat(self,j):
		return (1.0*j/self.MAXGRID_Y+0.5)*self.LAT_RANGE+self.LAT_MIN
'''

class GEO_DB:

	MAXGRID_X=200
	MAXGRID_Y=200


	description = None
	usrloc_db = None
	map_db = None

	DEN_MAX=0.0

	LONG_MIN=-122.327361
	LONG_MAX=-122.312425
	LONG_RANGE=0.0

	LAT_MAX=47.625556
	LAT_MIN=47.618333
	LAT_RANGE=0.0

	def __init__(self):
		#create database
		self.usrloc_db = pk.load('USERLOC.db',False)
		self.usrloc_db.dump()
		
		self.map_db = pk.load('GEOSPATIAL.db',False)
		#create grids
		for i in range(self.MAXGRID_X+1):
			for j in range(self.MAXGRID_Y+1):
				tmp=['dummy']
				self.map_db.set(str((i,j)),tmp)
		self.map_db.dump()
		self.LONG_RANGE = self.LONG_MAX - self.LONG_MIN
		self.LAT_RANGE = self.LAT_MAX - self.LAT_MIN
		self.load_usrloc()
		self.load_mapdb()

	def get_long_index(self, n):
		return 1.0*(n-self.LONG_MIN)/(self.LONG_RANGE/float(self.MAXGRID_X))

	def get_lat_index(self, n):
		return 1.0*(n-self.LAT_MIN)/(self.LAT_RANGE/float(self.MAXGRID_Y))

	def index2long(self,i):
		return (1.0*(i+0.5)/float(self.MAXGRID_X))*self.LONG_RANGE+self.LONG_MIN

	def index2lat(self,j):
		return (1.0*(j+0.5)/float(self.MAXGRID_Y))*self.LAT_RANGE+self.LAT_MIN

	def getUsrloc(self, uid):
		return self.usrloc_db.get(uid)

	def add_usrloc(self,uid,loc):
		self.usrloc_db.set(uid,loc)
		self.usrloc_db.dump()
		
	def rem_usrloc(self,uid):
		self.usrloc_db.rem(uid)
		self.usrloc_db.dump()

	def rem_mapdb(self,uid,loc):
		tmp = list(self.map_db.get(loc))
		tmp.remove(uid)
		self.map_db.set(loc, tmp)
		self.map_db.dump()

	def add_mapdb(self,uid,loc):
		#print (loc)
		#print (uid)
		tmp = list(self.map_db.get(loc))
		#print (tmp)
		#print (type(tmp))
		tmp.append(uid)
		if len(tmp)>self.DEN_MAX:
			self.DEN_MAX = len(tmp)
		self.map_db.set(loc, tmp)
		self.map_db.dump()	

	def update_info(self, uid,longitude, latitude):
		longitude=self.get_long_index(longitude)
		latitude=self.get_lat_index(latitude)
		#print '111'
		if DB_MUTEX.acquire():
			#print '222'
			curr_loc=getKey(longitude, latitude)
			#print '333'
			if haskey(uid, self.usrloc_db):
				#print '444'
				prev_loc=self.getUsrloc(uid)
				self.rem_mapdb(uid,prev_loc)
				self.rem_usrloc(uid)
				self.add_usrloc(uid,curr_loc)
				self.add_mapdb(uid,curr_loc)
			else:
				self.add_usrloc(uid,curr_loc)
				self.add_mapdb(uid,curr_loc)
			DB_MUTEX.release()

	def getGrid(self,loc):
		return 1.0*(len(self.map_db.get(loc))-1)/(max(self.DEN_MAX-1,1.0))*5.0

	def getDensity(self, loc):
		ans={}
		key_x=loc[0]
		key_y=loc[1]
		LB_x=max( key_x-25 , 0 )
		LB_y=max( key_y-25 , 0 )
		RB_x=min( key_x+25 , self.MAXGRID_X )
		RB_y=min( key_y+25 , self.MAXGRID_Y )
		ans['points']=[]
		for i in range(LB_x,RB_x):
			c_x=self.index2long(i)
			for j in range(LB_y,RB_y):
				c_y=self.index2lat(j)
				den=self.getGrid(str((i,j)))
				coord=[c_x,c_y]
				tmp_dic={}
				tmp_dic['coord']=coord
				tmp_dic['weight']=den
				if den>0.0:
					ans['points'].append(tmp_dic)
		return ans

	def getDensity_whole(self):
		ans={}
		ans['points']=[]
		for i in range(200):
			c_x=self.index2long(i)
			for j in range(200):
				c_y=self.index2lat(j)
				den=self.getGrid(str((i,j)))
				coord=[c_x,c_y]
				tmp_dic={}
				tmp_dic['coord']=coord
				tmp_dic['weight']=den
				if den>0.0:
					ans['points'].append(tmp_dic)
		#output=json.dump(ans)
		return ans

	def load_usrloc(self):
		try:
			self.usrloc_db = pk.load('USERLOC.db',False)
		except Exception,e:
			consoleMSG=getTimestamp()+"  ERROR: Failed to load user databse!"
			print (consoleMSG)
			sys.exit(0)

	def load_mapdb(self):
		#load database
		try:
			self.map_db = pk.load('GEOSPATIAL.db',False)
		except Exception,e:
			consoleMSG=getTimestamp()+"  ERROR: Failed to load spatial databse!"
			print (consoleMSG)
			sys.exit(0)