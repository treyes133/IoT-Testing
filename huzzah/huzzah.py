import socket,  time, network
from machine import Pin

echo = machine.Pin(14,machine.Pin.IN)
trig = machine.Pin(12,machine.Pin.OUT)
sta_if = network.WLAN(network.STA_IF)
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

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address = "192.168.4.3"

port = 324
server_address = (address, port)
sock.connect(server_address)

try:
    sock.setblocking(0)
except:
    print("error")

state = None
value = None

try:
    data = None
    while True:
        try:
            data = sock.recv(4)
        except:
            pass
        if data is not None or state is not None:
            if data is not None:
                state = data.decode()
                print(state)
                data = None
            if state == "rssi":
                #get rssi value
                value = sta_if.status("rssi")
            if state == "ultr":
                value = measurement(4)
            if state != "menu" and value is not None:
                message = str(value)[:3]
                print(message)
                sock.sendall(message.encode())

        time.sleep(0.1)
except:
    traceback.print_exc()
