import socket, struct
import sys
global led, lock
import pycom, binascii, network, threading
#imports

#turns off the pycom blue heartbeat
pycom.heartbeat(False)

ap_if = network.WLAN()
#sets the rgbled to a green color, green means start
pycom.rgbled(0x39FF14)

<<<<<<< HEAD
laptop_addr = ["192.168.4.2"]

thread_status = True

lock = Locking.lock()
=======
>>>>>>> 1f988bf8eddaac6d335d88dc3a50d1110daee1f8

def main():

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
	threads = []
	data_list = []
	client_list = []
	display_client = False
	display_clients = []
	#this function will run on the successful connection of a client
	conn,addr = sock.accept()

	while True:
		try:
			#print client address info
			print("client connected :: ",addr)
			if(addr is in laptop_addr and not display_client):
				t = threading.Thread(target = process, args = (conn,addr,sock,port,))
				t.start()
				display_clients.append(conn)
				display_client = True
			else:
				t = threading.Thread(target = data_client, args = (conn,addr,sock,len(data_list),))
				t.start()
				lock.aquire()
				data_list.append([])
				client_list.append(addr)
				lock.release()
			threads.append(t)
		finally:
			thread_status = False
			time.sleep(0.1)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def data_client(conn,addr,sock,index):
	global data_list
	global lock
	while thread_status:
		#receive data
		raw_msglen = sock.recv(4)
		if raw_msglen is None:
			pass
		else:
			msglen = struct.unpack('>I', raw_msglen)[0]
			data = recvall(sock,msglen)
			lock.aquire()

			#move binary data to signed input
			rssi = int(data.decode('utf8'))

			data_list[index].append(rssi)

			lock.release()

def process(conn,addr,sock,port):
	global data_list
	global client_list
	global display_clients
	global lock
	index = 0
	#breaks the connection if the exit command is called, or the client disconnects
	try:
		#while true loop to receive data
		while thread_status:
			#get data from connected devices
            #info = ap_if.status('stations')
            message = ""
			temp_list = []
			lock.aquire()
			for clients in data_list:
				if(len(clients)-1 is not index):
					if(len(clients)-2 >= 0):
						temp_list.append(clients[len(clients)-2])
					else:
						temp_list.append(1)
				else:
					temp_list.append(clients[len(clients)-1])
			lock.release()
			index += 1
            for x in range (0, len(client_list)):
                message += str(client_list[x])+","+str(temp_list[x])+";"
            msg_len = str(len(message))
			#sometimes data will be None, so if there is data, we need to process it
			for conn in display_client:
				conn.sendall(msg_len+"+"+message)

	finally:
		sock.close()


#runs the main function on an import
main()
