import socket, traceback, time
import numpy as np



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address = "localhost"

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
                value = np.random.choice(range(-50,-10,1), size=1)[0]
            if state == "ultr":
                value = np.random.choice(range(30,500,1), size=1)[0]
            if state != "menu" and value is not None:
                message = str(value)[:3]
                print(message)
                sock.sendall(message.encode())
                
        time.sleep(0.1)
except:
    traceback.print_exc()
