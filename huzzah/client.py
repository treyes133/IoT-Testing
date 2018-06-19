import sys
import socket
import time
from machine import Pin,Signal
import machine
#imoports

#setup the ADC on ADC channel 0 (the labeled ADC on board)
adc = machine.ADC(0)

#setup the selection pin as an input on gpio 15
selection_pin = machine.Pin(15, machine.Pin.IN)

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
		#read the ADC value
		adc_value = adc.read()
		print("adc_value",adc_value)
		#checks if the ADC value is actually non-zero
		if(adc_value not in range(0,50)):
			#different color ranges for different variable ranges
			if adc_value in range(60,160):
				color = "0xFF0000"
			if adc_value in range(161,260):
				color = "0xFF9900"
			if adc_value in range(261,360):
				color = "0xFFFE00"
			if adc_value in range(361,460):
				color = "0x36FF00"
			if adc_value in range(461,560):
				color = "0x00EDFF"
			if adc_value in range(561,660):
				color = "0x6F3CFF"
			if adc_value >= 601:
				color = "0xF800FF"
			#setup the output message
			message = 'led '+color
		else:
			#this is active when the ADC is basically zero

			#checks if the selection pin is high
			if(selection_pin.value() == 1):
				#sets the led message to blue
				message = 'led blue'
				led_status = -1
			else:
				#if not, then just alternate between 0 and 1 (green and red)
				if(led_status is 0):
					message = 'led green'
					led_status = 1
				else:
					message = 'led red'
					led_status = 0
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
