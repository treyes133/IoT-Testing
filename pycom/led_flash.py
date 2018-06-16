from machine import Pin,Signal
import machine

led_pin = machine.Pin(2,machine.Pin.OUT)
led = Signal(led_pin, invert = True)

selection_pin = machine.Pin(15, machine.Pin.IN)

while True:
	if(selection_pin.value() == 1):
		led.on()
	else:
		led.off()
