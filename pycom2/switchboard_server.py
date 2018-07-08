import socket
import sys, time
global led
import pycom, binascii, network, _thread, struct
#imports

print("test1")
class client:
	status = True
	socket = None
	address = None
	connection = None
	data_header = []
	data_label = []
	data_value = []
	hold_up = None
	t = None
	def __init__(self, sock, addr, conn):
		self.socket = sock
		self.address = addr
		self.connection = conn
		self.t = _thread.start_new_thread(self.start())

	def start(self):
		try:
			#nonblocking socket
			self.socket.setblocking(0)

			while(self.status is True):
				try:
					data = self.recv_msg(self.socket)
					temp = self.unpack(data,"+",";")
					recv_data_headers = temp[0]
					recv_data_labels = temp[1]
					recv_data_values = temp[2]



					self.data_header.append(recv_data_headers)
					self.data_label.append(recv_data_labels)
					self.data_value.append(recv_data_values)
				except Exception as exp:
					print(exp)
				if(len(self.data_label) > 0):
					if self.hold_up is None:
						self.hold_up = [self.data_header[0],self.data_label[0],self.data_value[0]]
						del self.data_header[0]
						del self.data_label[0]
						del self.data_value[0]
				time.sleep(0.001)
		except Exception as e:
			#client disconnected
			print("client ", self.address, " disconnected :: ",e)
			self.status = False
			while self.status is False:
				time.sleep(0.001)
		#after the above finishes, the thread will die
	def next_data(self):
		temp = self.hold_up
		self.hold_up = None
		return temp
	def recv_msg(self, sock):
		# Read message length and unpack it into an integer
		raw_msglen = recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return recvall(sock, msglen)

	def recvall(self, sock, n):
	    # Helper function to recv n bytes or return None if EOF is hit
	    data = b''
	    while len(data) < n:
	        packet = sock.recv(n - len(data))
	        if not packet:
	            return None
	        data += packet
	    return data
	def unpack(data,delimiter_sub,delimiter_break):
		data_header = []
		data_labels = []
		data_values = []
		while len(data) > 0:
			data_header.append(data[:data.index(delimiter_sub)])
			data = data[data.index(delimiter_sub)+1:]
			data_labels.append(data[:data.index(delimiter_sub)])
			data = data[data.index(delimiter_sub)+1:]
			data_values.append(data[:data.index(delimiter_break)])
			data = data[data.index(delimiter_break)+1:]
		return [data_header,data_labels,data_values]
class switchboard():
	status = True
	clients = []

	#[service,source,destination]
	stream = []
	t = None
	def __init__(self, clients):
		print("init")
		self.t = _thread.start_new_thread(self.main())
		self.clients = clients
		self.t.start()
		return
	def main(self):
<<<<<<< HEAD
<<<<<<< HEAD
		if(len(self.clients) > 0):
			for x in range(0,len(self.clients)):
				client = self.clients[x]
				#header, label, data
				client_data = client.next_data()
				if(client_data is not None):
					[dest, source, tag] = self.decompose_header(client_data[0])
					label = client_data[1]
					data = client_data[2]
					if(tag == "stream-request"):
						in_stream = False
						for contents in stream:
							#this case is the service is already streaming, so add to dest list
							if contents[0] is label and dest is contents[1] and source not in contents[2] and data is True:
								contents[2].append(source)
								in_stream = True
							if contents[0] is label and dest is contents[1] and source not in contents[2] and data is False:
								#in the stream and we want to remove
								del contents[2].index(source)
						#this service is not currently being requested from this client, so start a new service
						if not in_stream:
							self.stream.append([label,dest,source])
							self.single_packet(dest,tag,label,data,client.socket)
					if(tag == "stream-data"):
						#[service,source,destination] - stream
						for x in range(0,len(stream)):
							stream_service = stream[0]
							stream_source = stream[1]
							stream_dest = stream[2]
							if(stream_source is source and label is stream_service):
								client_destinations = stream_dest
								for x in range(0,len(client_destinations)):
									for client_object in self.clients:
										if client_destinations[x] is client_object.address:
											#sending the stream packet to the client
											self.stream_packet(client_destinations[x],stream_source,tag,label,data,client.socket)
					if(tag == "forward"):
						for client_object in self.clients:
							if(client_object.address is dest):
								self.single_packet_forward(source,dest,tag,label,data,client_object)
		else:
			time.sleep(0.001)
=======
=======
>>>>>>> bb58ea4ac82ab281c6bf2d01859b513f2fda341c
		print("main")
		while self.status is True:
			if(len(self.clients) > 0):
				for x in range(0,len(self.clients)):
					client = self.clients[x]
					#header, label, data
					client_data = client.next_data()
					if(client_data is not None):
						[dest, source, tag] = self.decompose_header(client_data[0])
						label = client_data[1]
						data = client_data[2]
						if(tag is "stream-request"):
							in_stream = False
							for contents in stream:
								#this case is the service is already streaming, so add to dest list
								if contents[0] is label and dest is contents[1] and source not in contents[2] and data is True:
									contents[2].append(source)
									in_stream = True
								if contents[0] is label and dest is contents[1] and source not in contents[2] and data is False:
									#in the stream and we want to remove
									#del contents[2].index(source)
									pass
							#this service is not currently being requested from this client, so start a new service
							if not in_stream:
								self.stream.append([label,dest,source])
								self.single_packet(dest,tag,label,data,client.socket)
						if(tag is "stream-data"):
							#[service,source,destination] - stream
							for x in range(0,len(stream)):
								stream_service = stream[0]
								stream_source = stream[1]
								stream_dest = stream[2]
								if(stream_source is source and label is stream_service):
									client_destinations = stream_dest
									for x in range(0,len(client_destinations)):
										for client_object in self.clients:
											if client_destinations[x] is client_object.address:
												#sending the stream packet to the client
												self.stream_packet(client_destinations[x],stream_source,tag,label,data,client.socket)
						if(tag is "forward"):
							for client_object in self.clients:
								if(client_object.address is dest):
									self.single_packet_forward(source,dest,tag,label,data,client_object)
			else:
				time.sleep(0.001)
<<<<<<< HEAD
>>>>>>> b21048e8d1ffc28366a7895f2b52cd82c1379f26
=======
>>>>>>> bb58ea4ac82ab281c6bf2d01859b513f2fda341c
	def single_packet_forward(self, source, destination, tag, label, data, sock):
		header = dest+","+"server"+","+tag
		message = header+"+"+label+"+"+data+";"
		msg = struct.pack(">I", len(message)) + message
		sock.sendall(msg)

	def stream_packet(self, destination, source, tag, label, data, sock):
		header = dest+","+source+","+tag
		message = header+"+"+label+"+"+data+";"
		msg = struct.pack(">I", len(message)) + message
		sock.sendall(msg)

	def single_packet(self, dest, tag, label, data, sock):
		header = dest+","+"server"+","+tag
		message = header+"+"+label+"+"+data+";"
		msg = struct.pack(">I", len(message)) + message
		sock.sendall(msg)

	def decompose_header(self, header):
		destination = header[:header.index(",")]
		header = header[header.index(",")+1:]

		source = header[:header.index(",")]
		header = header[header.index(",")+1:]

		label = header

		return [destination,source,label]




	def update_clients(self, new_list):
		self.clients = new_list
		remove_index = []
		for c in range(0,len(self.clients)):
			if self.clients[c].status is False:
				remove_index.append(c)
				self.clients[c].status = True
		for x in range(len(remove_index)-1,-1,-1):
			del self.clients[x]
		return remove_index

#turns off the pycom blue heartbeat
pycom.heartbeat(False)

ap_if = network.WLAN()
#sets the rgbled to a green color, green means start
pycom.rgbled(0x39FF14)

print("test1")

#setup port and socket
port = 324
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind to port
server_address = ('', port)
sock.bind(server_address)

#start the listening process

print("test2")
#start the client acceptance system
print("accepting clients on port ",port)
clients = []

switch_board = switchboard(clients)
print("test3")
while True:
	try:
		sock.listen(1)
		conn,addr = sock.accept()
		#print client address info
		print("client connected :: ",addr)
		clients.append(client(sock,addr,conn))
		clients[len(clients)-1].start()
		remove_index = switch_board.update_clients(clients)
		for x in range(len(remove_index)-1,-1,-1):
			del clients[x]
	except Exception as exc:
		print(exc)
	finally:
		for client in clients:
			client.status = False
