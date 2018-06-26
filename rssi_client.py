import sys,socket,time
import numpy as np
import matplotlib.pyplot as plt


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

address = "192.168.4.1"

port = 324
server_address = (address, port)
sock.connect(server_address)
mac_addr = []
rssi = []
def recv_data(sock):
    msglen = ""
    data = sock.recv(1)
    while data is not "+":
        msglen += data
        data = sock.recv(1)
    #might need a conversion here from binary to integer length
    final_data = ""
    data_length = 1024
    while msglen >= data_length:
        final_data += sock.recv(1024)
        msglen -= data_length
    final_data += sock.recv(msglen)

    mac_addr = []
    rssi = []
    #move from string to list
    while len(final_data) > 0:
        mac_addr.append(final_data[:final_data.index(",")])
        rssi.append(final_data[final_data.index(",")+1:final_data.index(";")])
        final_data = final_data[final_data.index(";")+1:]
    return [mac_addr,rssi]

try:
    while True:
        [mac_addr_n, rssi_n] = recv_data(sock)
        for x in mac_addr_n:
            mac_addr.append(x)
        for y in rssi_n:
            rssi.append(y)
        
finally:
    print("exiting")
