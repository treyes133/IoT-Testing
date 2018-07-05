import socket
import sys
global led,
import pycom, binascii, network,threading,struct
#imports

class client(threading.Thread):
	self.status = True
	self.socket = None
	self.address = None
	self.connection = None
	self.data_label = []
	self.data_value = []
	self.hold_up = None
	def __init__(self, sock, addr, conn):
		threading.Thread.__init__(self)
		self.socket = sock
		self.address = addr
		self.connection = conn

	def start(self):
		try:
			#nonblocking socket
			self.socket.setblocking(0)

			while(self.status is True):
				try:
		            data = recv_msg(sock)
		            [recv_data_labels,recv_data_values] = unpack(data,"+",";")
					self.data_label.append(recv_data_labels)
					self.data_value.append(recv_data_values)
		        except:
		            #no data
		            pass
				if(len(self.data_label) > 0):
					if self.hold_up is None:
						self.hold_up = [self.data_label[0],self.data_value[0]]
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
	def unpack(self, data,delimiter_label,delimiter_value):
	    data_labels = []
	    data_values = []
	    while len(data) > 0:
	        data_labels.append(data[:data.index(delimiter_label)]
	        data_values.append(data[data.index(delimiter_label)+1:data.index(delimiter_value)])
	        data = data[data.index(delimiter_value)+1:]
	    return [data_labels,data_values]
class switchboard(threading.Thread):
	self.status = True
	self.clients = []
	def __init__(self, clients):
		threading.Thread.__init__(self)
		self.clients = clients
	def main(self):
		if(len(self.clients) > 0):
			#add a third packet to the message, a source, destination, and packet tag
		else:
			time.sleep(0.01)
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



#setup port and socket
port = 324
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind to port
server_address = ('', port)
sock.bind(server_address)
#start the listening process
sock.listen(1)
#start the client acceptance system
print("accepting clients on port ",port)
switch_board = switchboard()
clients = []
switch_board = switchboard(clients)
while True:
	try:
		conn,addr = sock.accept()
		#print client address info
		print("client connected :: ",addr)
		clients.append(client(sock,addr,conn))
		clients[len(clients)-1].start()
		remove_index = switch_board.update_clients(clients)
		for x in range(len(remove_index)-1,-1,-1):
			del clients[x]

	finally:
		for client in clients:
			client.status = False
