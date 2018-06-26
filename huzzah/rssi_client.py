import sys,socket,time,machine,network
from machine import Pin, Signal


sta_if = network.WLAN(network.STA_IF)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

address = "192.168.4.1"

port = 324
server_address = (address, port)
max = 30
min = 10
sock.connect(server_address)

try:
    while True:
        rssi = sta_if.status("rssi")*-1
        if(max < rssi):
            max = rssi
        step = int((max-min)/7)
        print(rssi)
        if(rssi in range(6,12)):
            color = "0xFF9900"
        elif(rssi in range(13,20)):
        	color = "0xFFFE00"
        elif(rssi in range(21,28)):
        	color = "0x36FF00"
        elif(rssi in range(29,38)):
        	color = "0x00EDFF"
        elif(rssi in range(39,50)):
        	color = "0x6F3CFF"
        else:
            color = "0xF800FF"
        message = 'led '+color
        print(message)
        sock.sendall(message)

        data = sock.recv(16)
        time.sleep(0.01)
finally:
    print("exiting")
