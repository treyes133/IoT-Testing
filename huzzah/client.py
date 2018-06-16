import sys
import socket
import time
from machine import Pin,Signal
import machine


selection_pin = machine.Pin(15, machine.Pin.IN)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = "192.168.4.1"
port = 324
server_address = (address, port)

print("connecting to ",address," on port ",port)

sock.connect(server_address)
led_status = 0
try:
	while True:
		print(selection_pin.value())
		if(selection_pin.value() == 1):
			message = 'led blue'
			led_status = -1
		else:
			if(led_status is 0):
				message = 'led green'
				led_status = 1
			else:
				message = 'led red'
				led_status = 0

		sock.sendall(message)
		print("message sent!")
		data = sock.recv(16)
		if(data):
			print("message received! :: ",data)
		time.sleep(1)
finally:
    sock.close()
