import machine,time
from machine import Pin


activate_pin = machine.Pin("G22",machine.Pin.OUT)

try:
    while True:
        activate_pin.toggle()
        time.sleep(1)
        activate_pin.toggle()
finally:
    pass
