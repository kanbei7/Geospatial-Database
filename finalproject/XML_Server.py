#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import geospatialDB as geo

LONG_MIN=-122.327361
LONG_MAX=-122.312425
LAT_MAX=47.625556
LAT_MIN=47.618333

def normalize_long(n):
	n=max(LONG_MIN,n)
	n=min(LONG_MAX,n)
	return n

def normalize_lat(n):
	n=max(LAT_MIN,n)
	n=min(LAT_MAX,n)
	return n

def fork(server):
	server.db=geo.GEO_DB()

class KeyValueServer:
	db=None
	_rpc_methods_ = ['get', 'set']
	#cluster_ip=[]
	'''
	def sync():
		
	'''

	def __init__(self, address):
		self._data = {}
		self._serv = SimpleXMLRPCServer(address, allow_none = True)
		for name in self._rpc_methods_:
			self._serv.register_function(getattr(self,name))
	
	def get(self):
		return self.db.getDensity_whole()

	def set(self, uid, longitude,latitude):
		longitude=normalize_long(longitude)
		latitude=normalize_lat(latitude)
		self.db.update_info(uid,longitude,latitude)
		print "set complete!"

	def serve_forever(self):
		self._serv.serve_forever()


if __name__ == '__main__':
	kvserv = KeyValueServer(('', 8200))
	fork(kvserv)
	print "Server up!"
	kvserv.serve_forever()

#server.register_instance(MyFuncs())
print "Server up!"

# Run the server's main loop
#server.serve_forever()