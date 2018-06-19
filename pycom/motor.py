import machine,time
from machine import Pin


activate_pin = machine.Pin("G4",machine.Pin.OUT)

try:
    while True:
        activate_pin.toggle()
        print("on")
        time.sleep(10)
        activate_pin.toggle()
        print("off")
        time.sleep(10)
finally:
    pass
