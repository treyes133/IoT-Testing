import socket
import sys
global led
import pycom, binascii, network
#imports

#turns off the pycom blue heartbeat
pycom.heartbeat(False)

ap_if = network.WLAN()
#sets the rgbled to a green color, green means start
pycom.rgbled(0x39FF14)

laptop_mac = "34-02-86-91-AD-B6"

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
	#this function will run on the successful connection of a client
	conn,addr = sock.accept()
	while True:
		try:
			#print client address info
			print("client connected :: ",addr)
			process(conn,addr,sock,port)
		finally:
			conn.close()



def process(conn,addr,sock,port):
	#breaks the connection if the exit command is called, or the client disconnects
	try:
		#while true loop to receive data
		while True:
			#get data from connected devices
            info = ap_if.status('stations')
            message = ""
            for i in info:
                if(info[0] is not laptop_mac):
                    message += str(info[0])+","+str(info[1])+";"
            msg_len = str(len(message))
			#sometimes data will be None, so if there is data, we need to process it
			conn.sendall(msg_len+"+"+message)

	finally:
		sock.close()


#runs the main function on an import
main()
