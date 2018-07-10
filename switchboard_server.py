import socket
import sys, time
import  binascii, threading, struct, traceback
#imports

print("test1")
class client(threading.Thread):
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
		threading.Thread.__init__(self)
		self.socket = sock
		self.address = addr[0]
		self.connection = conn

	def run(self):
		try:
			#nonblocking socket
			self.socket.setblocking(0)

			while(self.status is True):
				try:
					#print("receiving data")
					data = self.recv_msg(self.connection)
					if data is not None:
						print("unpacking data")
						temp = self.unpack(data,"+",";")
						print("parsing data")
						recv_data_headers = temp[0]
						recv_data_labels = temp[1]
						recv_data_values = temp[2]


						print("added to hold up")
						self.data_header.append(recv_data_headers)
						self.data_label.append(recv_data_labels)
						self.data_value.append(recv_data_values)
						print(self.status)
				#except(socket.error):
				#	if e.errno is errno.ECONNRESET:
				#		print("Client disconnected")
				#		self.status = False
				#		while self.status is False:
				#			time.sleep(0.001)
				#		self.status = False
				except Exception as exp:
					#print(exp)
					pass
				if(len(self.data_label) > 0):
					if self.hold_up is None:
						self.hold_up = [self.data_header[0],self.data_label[0],self.data_value[0]]
						del self.data_header[0]
						del self.data_label[0]
						del self.data_value[0]
				time.sleep(0.001)
		except:
			#client disconnected
			print("client ", self.address, " disconnected :: ")
			traceback.print_exc()
			self.status = False
			while self.status is False:
				time.sleep(0.001)
		print("Thread closing ",self.address)
		#after the above finishes, the thread will die
	def next_data(self):
		temp = self.hold_up
		self.hold_up = None
		#print("Hold up pulled")
		return temp
	def recv_msg(self, sock):
		# Read message length and unpack it into an integer
		raw_msglen = self.recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return self.recvall(sock, msglen).decode('utf-8')

	def recvall(self, sock, n):
	    # Helper function to recv n bytes or return None if EOF is hit
	    data = b''
	    while len(data) < n:
	        packet = sock.recv(n - len(data))
	        if not packet:
	            return None
	        data += packet
	    return data
	def unpack(self,data,delimiter_sub,delimiter_break):
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
class switchboard(threading.Thread):
	status = True
	clients = []

	#[service,source,destination]
	stream = []
	def __init__(self, clients):
		threading.Thread.__init__(self)
		self.clients = clients
		print("Switchboard active!")
	def run(self):
		print("main")
		while self.status is True:
			if(len(self.clients) > 0):
				for x in range(0,len(self.clients)):
					client = self.clients[x]
					#header, label, data
					client_data = client.next_data()
					if(client_data is not None):
						print("hold up has value")
						[dest, source, tag] = self.decompose_header(client_data[0][0])
						label = client_data[1][0]
						data = bool(client_data[2])
						print(data)
						print(label)
						print(tag)
						if(tag == "stream-request"):
							print("stream-request")
							in_stream = False
							for contents in self.stream:
								#this case is the service is already streaming, so add to dest list
								if contents[0] is label and dest is contents[1] and source not in contents[2] and data is True:
									contents[2].append(source)
									in_stream = True
									print("added to stream")
								if contents[0] is label and dest is contents[1] and source not in contents[2] and data is False:
									#in the stream and we want to remove
									#del contents[2].index(source)
									print("removing from stream")
									pass
							#this service is not currently being requested from this client, so start a new service
							print("instream",in_stream)
							if not in_stream and data is True:
								self.stream.append([label,dest,source])
								print("creating new stream")
								for client in self.clients:
									print(client.address)
									print(dest)
									if client.address == dest:
										self.single_packet(dest,tag,label,data,client.connection)
										#print("packet sent",dest,client.address)
										break
						if(tag == "stream-data"):
							#[service,source,destination] - stream
							print("looking for forward data")
							for x in range(0,len(self.stream)):
								stream_service = self.stream[x][0]
								stream_source = self.stream[x][1]
								stream_dest = self.stream[x][2]
								if(stream_source is source and label is stream_service):
									client_destinations = stream_dest
									print(client_destinations)
									for x in range(0,len(client_destinations)):
										print("destination",client_destinations[x])
										for client_object in self.clients:
											if client_destinations[x] is client_object.address:
												#sending the stream packet to the client
												print("client found, forwarding packet")
												self.stream_packet(client_destinations[x],stream_source,tag,label,data,client.socket)
						if(tag == "forward"):
							for client_object in self.clients:
								if(client_object.address is dest):
									self.single_packet_forward(source,dest,tag,label,data,client_object)
			else:
				time.sleep(0.001)
	def single_packet_forward(self, source, destination, tag, label, data, sock):
		header = dest+","+"server"+","+tag
		message = header+"+"+label+"+"+data+";"
		message = bytes(message.encode('utf-8'))
		msg = struct.pack('>I', len(message)) + message 
		sock.sendall(msg)

	def stream_packet(self, destination, source, tag, label, data, sock):
		header = dest+","+source+","+tag
		message = header+"+"+label+"+"+data+";"
		message = bytes(message.encode('utf-8'))
		msg = struct.pack('>I', len(message)) + message 
		sock.sendall(msg)
		print("message sent ::",destination)

	def single_packet(self, dest, tag, label, data, sock):
		
		header = dest+","+"server"+","+tag
		message = header+"+"+label+"+"+str(data)+";"
		print(message)
		message = bytes(message.encode('utf-8'))
		msg = struct.pack('>I', len(message)) + message 
		sock.sendall(msg)
		print("packet sent")
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
switch_board.start()
print("test3")
while True:
	try:
		sock.listen(1)
		conn,addr = sock.accept()
		#print client address info
		print("client connected :: ",addr)
		new_client = client(sock,addr,conn)
		clients.append(new_client)
		new_client.start()
		print("forked client")
		remove_index = switch_board.update_clients(clients)
		for x in range(len(remove_index)-1,-1,-1):
			del clients[x]
	except Exception as exc:
		#print(exc)
		pass
for client in clients:
	client.status = False
	print("clients closing")
