import network
import time
from machine import Pin,Signal
import machine
#imports

#sets up the STA and access point objects
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

#turns off the access point, we don't need it right now
ap_if.active(False)

#timeout setup
time_loop = 0
#if it isn't already connected, start the process to connect
if not sta_if.isconnected():
		print('connecting to network...')
		#makes sure the STA is actually enabled
		sta_if.active(True)
		#our network we are connecting to is called Pycom, with no password
		sta_if.connect('Pycom', '')
		#a while loop to wait for connection
		while not sta_if.isconnected() and time_loop <= 10000:
			time_loop += 1
			time.sleep(0.001)
#prints out the network configuration
print('network config:', sta_if.ifconfig())
