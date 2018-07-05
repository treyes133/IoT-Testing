import sys,socket,time,threading,_thread
import numpy as np
import matplotlib.pyplot as plt


lock = threading.Lock()

#server socket setup (client)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

address = "192.168.4.1"

port = 324
server_address = (address, port)
sock.connect(server_address)

