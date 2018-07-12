import time, os, threading, socket, struct, cPickle

from threading import Thread



def recvall(sock, n):
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


class ThreadAccept:
	def __init__(self, port):
		self.HOST = ''
		self.PORT = port
		self.connected = []
		self.children = []
		self.client = None
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.bind((self.HOST,self.PORT))
		self.s.setblocking(0)
		self.stopped = False
		self.names = []
	def start(self):
		Thread(target=self.update,args=()).start()
		return self
	def update(self):
		while not self.stopped:
			try:
				self.s.listen(1)
				conn, addr = self.s.accept()
				print('new connection :: ',addr)
				valid_name = False
				while not valid_name:
					name = conn.recv(1024)
					print('name :: ', name)
					if name in self.names:
						conn.sendall("name already taken")
					else:
						names.append(name)
				conn.sendall("connected")
				services = conn.recv(1024).split(',')
				connection = [conn,name,services]
				client = ThreadReceive(conn).start()
				child = [client,connection]
				self.connected.append(child)
			except:
				pass
		for children in self.connected:
			children[0].stop()
		print "killed all child threads"
		print "acceptor exiting"
	def get_connections(self):
		return self.connected
	def check_child_status(self):
		for a in range(0,len(self.connected)):
			if self.connected[a][0].disconnect is True:
				del self.connected[a]
				print "removed thread"
	def exit(self):
		self.stopped = True

class ThreadReceive:
	def __init__(self, connection):
		self.conn = connection
		self.disconnect = False
		self.master_list = []
		self.current = None
		self.close = False
	def recvall(socket, n):
		data = ''
		while len(data) < n:
			packet = sock.recv(n - len(data))
		    	if not packet:
		    		return None
			data += packet
		return data
	def start(self):
		Thread(target=self.update,args=()).start()
		return self
	def update(self):
		time.sleep(0.001)
		try:
		    while self.close is False:
			#this messsage is from the server, and contains the list of all connected clients
			raw_msg = recvall(self.conn,5)
			if raw_msg:
				#c == label
				#I == packet length
				label = struct.unpack('>cI', raw_msg)[0]
				msglen = struct.unpack('>cI', raw_msg)[1]

				data = cPickle.loads(recvall(self.conn,msglen))
				self.master_list.append(data)
			if self.current is None and len(self.master_list) > 0:
				self.current = self.master_list[0]
				del self.master_list[0]
			time.sleep(0.001)
               	except socket.error, exc:
			print "disconnected"
			self.disconnect = True
		print "child exiting"
	def get_data(self):
		if self.current is not None:
			temp = self.current
			self.current = None
			return temp
		else:
			return None
	def stop(self):
		self.close = True
	def disconnect(self):
		return self.disconnect
accept = ThreadAccept(1890).start()
connected = []
label = []
c_string = ""
stream_list = []
packet_stream = ['b','d']
packet_direction = ['f','g']
packet_stream_request = ['a','c']
packet_else = ['l']
packet_lookup = {'a':'b','c':'d'}
packet_request = {'a':'v','c':'w','b':'a','d':'c'}
def string_send_connect():
	for name in connected:
		c_string += name+";"
	c_string = c_String[:-1]
	return c_string
try:
	while True:
		clients = accept.get_connections()
		accept.check_child_status()
		if len(clients) > 0:
			try:
				for c in range(0,len(clients)):
					data = clients[c][0].get_data()
					if data is not None:
						#this means that there was some packet waiting in the get_data buffer
						#packet data is already [source, destination, label, [payload]]
						source = data[0]
						destination = data[1]
						label = data[2]
						packet_contents = data[3]
						if label in packet_stream_request:
							state_code = data[4]
							redundency = False
							added = False
							remove = False
							for item in stream_list:
								for destination_from_list in item[1]:
									if packet_contents == item[0] and source == destination_from_list and label == item[2]:
										#already being requested, no action taken
										if state_code == 0:
											#this means to remove from list
											remove = True
										redundency = True
								if remove:
									try:
										item[1].remove(source)
									except:
										print "could not remove from list"
							if not redundency and state_code == 1:
								for item in stream_list:
									if source == item[0] and label == item[2]:
										#this means that the source is already being requested, so add it to the destination list
										added = True
										item[1].append(source)
								if not added:
									#this means that the source is not being requested, so we make a new entry in route_list
									#this looks backwards but is correct
									stream_list.append([packet_contents,source,packet_lookup[label]])
									#we need to request this data, so sending packet to start the request process
									for x in range(0,len(clients)):
										if clients[x][1][1] == packet_contents:
											#this is the right source
											packet = cPickle.dumps(['server',packet_contents,packet_request[label],1])
											msg = struct.pack('>cI',packet_request[label],len(packet))+packet
											clients[x][1][0].sendall(msg)
											print label+" request sent!"
									added = True
							if added:
								print "stream list appended!"
						if label in packet_direction:
							for x in range(0,len(clients)):
								if clients[x][1][1] == destination:
									pickled = cPickle.dumps(data)
									msg = struct.pack('>cI',label,len(pickled))+pickled
									clients[x][1][0].sendall(msg)
						if label in packet_else:
							if label == 'l':
								names = ""
								for x in range(0,len(clients)):
									names+=clients[x][1][1]+";"
								names = names[:-1]
								packet = cPickle.dumps(['server',source,'l',names])
								msg = struct.pack('>cI',label,len(packet))+packet
								destination = source
								for x in range(0,len(clients)):
									if clients[x][1][1] == destination:
										clients[x][1][0].sendall(msg)
										print "message sent"

						if label in packet_stream:
							for x in stream_list:
								if source == x[0] and label == x[2]:
									#this means we have found the right forward section for the route
									destination_list = x[1]
									#destination_list is the names of the clients this needs to be forwarded to, need to do lookup to find each
									for y in range(0,len(clients)):
										if clients[y][1][1] in destination_list:
											#this means that the name is in the list
											packet = cPickle.dumps(['server',clients[y][1][1],label,packet_contents])
											msg = struct.pack('>cI',label,len(packet))+packet
											clients[y][1][0].sendall(msg)
						for item in stream_list:
							#checks for empty stream requests
							print item
							if len(x[1]) == 0:
								for y in range(0,len(clients)):
									if clients[y][1][1] == x[0]:
										 #means that this y is the right client, so we need to send a stop packet to this client
										 conn = clients[y][1][0]
										 #found the client, now reverse search the service to find the right label
										 label = packet_request[x[2]]
										 packet = cPickle.dumps(['server',clients[y][1][1],label,0])
										 msg = struct.pack('>cI', label, len(packet))+packet
										 conn.sendall(msg)
										 print "killed request for streaming feed"
			except Exception as e:
				print "there was an exception\n",e
		time.sleep(0.01)


except KeyboardInterrupt:
	print "exiting"

accept.exit()

print "done."
