import sys

import socket

import time

from machine import Pin,Signal

import machine

import network

sta_if = network.WLAN(network.STA_IF)


#imoports


#setup client socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = "192.168.4.1"

port = 324

server_address = (address, port)



print("connecting to ",address," on port ",port)


#connects to server
sock.connect(server_address)


#initialize the LED status variable
led_status = 0

try:

	#infinite loop
	while True:
        rssi = sta_if.status("rssi")*-1


        if rssi in range(6,12):
        	color = "0xFF9900"
        if rssi in range(13,20):
        	color = "0xFFFE00"
        if rssi in range(21,28):
        	color = "0x36FF00"
        if rssi in range(29,38):
        	color = "0x00EDFF"
        if rssi in range(39,50):
        	color = "0x6F3CFF"
        if rssi >= 51:
        	color = "0xF800FF"
			#setup the output message
		message = 'led '+color

		#sends the message across the socket
		sock.sendall(message)

		print("message sent!")

		#does a blocking wait to receive a return message of 16 bits
		data = sock.recv(16)

		if(data):

			#if there is a valid return on data, print what was received
			print("message received! :: ",data)

		#wait for 1 second before restarting
		time.sleep(1)

finally:

	#on exit, close the socket
    sock.close()
