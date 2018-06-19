
from machine import I2C
from machine import Pin
import machine, time

import machine
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))


device_address = i2c.scan()[0]
print(device_address)


write = i2c.readfrom_mem(device_address, 6,8)
print(write)
