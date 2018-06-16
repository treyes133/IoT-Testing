import sys
import socket
import time
from machine import Pin,Signal
import machine

adc = machine.ADC(0)
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
		adc_value = adc.read()
		print("adc_value",adc_value)
		if(adc_value not in range(0,5)):
			if adc_value in range(6,100):
				color = "0xFF0000"
			if adc_value in range(101,200):
				color = "0xFF9900"
			if adc_value in range(201,300):
				color = "0xFFFE00"
			if adc_value in range(301,400):
				color = "0x36FF00"
			if adc_value in range(401,500):
				color = "0x00EDFF"
			if adc_value in range(501,600):
				color = "0x6F3CFF"
			if adc_value >= 601:
				color = "0xF800FF"
			print("color :: ",color)
			message = 'led '+color

		else:
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
