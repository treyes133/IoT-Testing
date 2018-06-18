from machine import I2C
from machine import Pin
import machine, time

i2c = I2C(0, pins=('G15','G10'))     # create and use non-default PIN assignments (P10=SDA, P11=SCL)
i2c.init(I2C.MASTER, baudrate=20000) # init as a master

i2c.scan()
