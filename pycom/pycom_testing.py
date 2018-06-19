from machine import I2C


i2c = I2C(0, I2C.MASTER, pins=('P9','P10'))

i2c.init(I2C.MASTER, baudrate=20000)

i2c.scan()
