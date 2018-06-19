from machine import Pin

import machine, time


motor_pin = machine.Pin("G22",machine.Pin.OUT)

try:
    while True:
        print("on")
        motor_pin.toggle()
        time.sleep(3)
        print("off")
        motor_pin.toggle()
        time.sleep(3)
finally:
    pass
