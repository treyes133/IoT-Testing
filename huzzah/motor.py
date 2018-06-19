import machine,time
from machine import Pin


activate_pin = machine.Pin(15,machine.Pin.OUT)

try:
    while True:
        activate_pin.on()
        print("on")
        time.sleep(3)
        activate_pin.off()
        print("off")
        time.sleep(3)
finally:
    pass
