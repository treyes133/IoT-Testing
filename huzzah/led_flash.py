from machine import Pin,Signal
import machine
#imports

#sets up the led, which is on pin 2 and is an output
led_pin = machine.Pin(2,machine.Pin.OUT)

#setup the led pin, and we need to invert this since our hardware is inverted
led = Signal(led_pin, invert = True)

#sets up the selection pin, on pin 15, and sets it as a input
selection_pin = machine.Pin(15, machine.Pin.IN)
print("running with checker on 15")
while True:
	#if the pin value is "high" aka 1
	if(selection_pin.value() == 1):
		#turn on the LED
		led.on()
	else:
		#turn off the LED
		led.off()
