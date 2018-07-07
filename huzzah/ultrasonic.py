from machine import Pin,Signal
import utime, machine

echo = machine.Pin(14,machine.Pin.IN)
trig = machine.Pin(12,machine.Pin.OUT)

trig.off()
utime.sleep(3)

def measurement(avg):

    global echo
    global trig
    measurements = []
    for x in range(0,avg+1):
        trig.on()
        utime.sleep_us(10)
        trig.off()
        pulse_start=0
        pulse_end=0
        timeout = 10000
        while echo.value() is 0 and timeout > 0:
            pulse_start = utime.ticks_us()
            timeout -= 1

        timeout = 10000
        while echo.value() is 1 and timeout > 0:
            pulse_end = utime.ticks_us()
            timeout -=1
        if timeout > 0:
            pulse_duration = utime.ticks_diff(pulse_end,pulse_start)/(pow(10,6))
            distance = pulse_duration * 17150

            distance = round(distance, 2)
            measurements.append(distance)
        else:
            measurements.append(0)


    utime.sleep_us(10)
    return sum(measurements)/len(measurements)
