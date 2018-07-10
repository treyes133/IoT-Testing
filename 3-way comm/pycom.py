import socket, time
import traceback



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address = "localhost"

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
                print(color)
            if color == "led blu":
                print(color)
            if color == "led red":
                print(color)
        time.sleep(0.01)
except:
    traceback.print_exc()
