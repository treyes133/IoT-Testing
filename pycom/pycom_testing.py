<<<<<<< HEAD
from machine import I2C
=======
from machine import Pin
>>>>>>> 5944e578116339da15720474254d3e65e85c8ab4

import machine, time

<<<<<<< HEAD
i2c = I2C(0, I2C.MASTER, pins=('P9','P10'))

i2c.init(I2C.MASTER, baudrate=20000)

i2c.scan()
=======

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
>>>>>>> 5944e578116339da15720474254d3e65e85c8ab4
