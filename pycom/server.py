import socket
import sys
global led
import pycom
pycom.heartbeat(False)
pycom.rgbled(0xF333FF)
def main():

	port = 324
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('', port)
	sock.bind(server_address)
	sock.listen(1)
	accept_connection(sock,port)
def accept_connection(sock, port):
	print("accepting clients on port ",port)
	conn,addr = sock.accept()
	while True:
		try:
			print("client connected :: ",addr)
			receive_data(conn,addr,sock,port)
		finally:
			conn.close()
def receive_data(conn,addr,sock,port):
	while True:
		data = conn.recv(16)
		if(data):
			print("data received :: ",data)
			process_data(data)
			conn.sendall(data)
		else:
			break
def process_data(data):
	global led

	if(data == b'led green'):
		pycom.rgbled(0x007f00)
	if(data == b'led red'):
		pycom.rgbled(0x7f0000)
	if(data == b'led blue'):
		pycom.rgbled(0x0000ff)

	return False
main()
