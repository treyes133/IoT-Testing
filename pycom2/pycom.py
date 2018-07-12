import socket, time
import pycom

pycom.heartbeat(False)
pycom.rgbled(0xF333FF)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address = "192.168.4.3"
port = 324
server_address = (address, port)
sock.connect(server_address)

sock.setblocking(0)

state = None

try:
    while True:
        data = None
        try:
            data = sock.recv(7)
        except:
            pass
            #traceback.print_exc()
        color = data
        if color is not None:
            print(color)
            color = color.decode()
            if color == "led gre":
                pycom.rgbled(0x007f00)
            if color == "led blu":
                pycom.rgbled(0x0000ff)
            if color == "led red":
                pycom.rgbled(0x7f0000)
        time.sleep(0.01)
except:
    traceback.print_exc()
