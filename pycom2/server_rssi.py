import socket
import sys
global led
import pycom, binascii
#imports

#turns off the pycom blue heartbeat
pycom.heartbeat(False)

#sets the rgbled to a purple color
pycom.rgbled(0xF333FF)


def main():

	#setup port and socket
	port = 324
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#bind to port
	server_address = ('', port)
	sock.bind(server_address)
	#start the listening process
	sock.listen(1)
	accept_connection(sock,port)
def accept_connection(sock, port):
	#start the client acceptance system
	print("accepting clients on port ",port)
	#this function will run on the successful connection of a client
	conn,addr = sock.accept()
	while True:
		try:
			#print client address info
			print("client connected :: ",addr)
			receive_data(conn,addr,sock,port)
		finally:
			conn.close()
def receive_data(conn,addr,sock,port):
	#breaks the connection if the exit command is called, or the client disconnects
	try:
		#while true loop to receive data
		while True:
			#data receiving function
			data = conn.recv(16)
			if(data):
				#sometimes data will be None, so if there is data, we need to process it
				print("data received :: ",data)
				process_data(data)
				conn.sendall(data)
			else:
				break
	finally:
		sock.close()
def process_data(data):
	#process the data, and change LED based on input
	if(data == b'led green'):
		pycom.rgbled(0x007f00)
	if(data == b'led red'):
		pycom.rgbled(0x7f0000)
	if(data == b'led blue'):
		pycom.rgbled(0x0000ff)
	if("0x" in data):
		#all the data is sent in binary mode, which we need to decode to get the string version of the data
		data = data.decode('utf-8')
		print(data)
		#gets rid of the 'led 0x', and typecasts it in base 16 (aka hex)
		color = int(data[data.index("x")+1:],16)
		#sets the color
		pycom.rgbled(color)
	return False

#runs the main function on an import
main()
