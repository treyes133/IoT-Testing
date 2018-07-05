import sys,socket,time,machine,network,struct
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
        rssi = sta_if.status("rssi")
        message = str(rssi)
        msg_len = len(message)
        msglen = struct.pack(">I",msg_len)
        data_packet = msglen+message
        print(data_packet)
        sock.sendall(data_packet)
        time.sleep(0.01)
finally:
    print("exiting")
