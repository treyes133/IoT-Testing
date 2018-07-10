import threading,traceback,socket,time,msvcrt
import numpy as np
import matplotlib.pyplot as plt
class plotter(threading.Thread):
    import matplotlib.pyplot as plt
    import numpy as np
    
    rssi_data = []
    ultrasonic_data = []
    li_obj = None
    state = None

    change = False
    time_start = time.time()
    delay = 0.01
    x_data = []
    ax = None

    graph = False
    
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        fig = plt.figure()
        self.ax = fig.add_subplot(111)
        while True:
            if(self.change is False and self.state is not None):
                   #for x in range(len(self.x_data) ,len(self.rssi_data)):
                     #  self.x_data.append(time.time()-self.time_start)
                self.x_data.append(time.time()-self.time_start)
                self.ax.legend([self.state])
                self.li_obj.set_xdata(self.x_data)
                
                if(self.state == "rssi"):
                    self.li_obj.set_ydata(self.rssi_data)
                    print(len(self.rssi_data))
                if(self.state == "ultrasonic"):
                    self.li_obj.set_ydata(self.ultrasonic_data)
                    print(len(self.ultrasonic_data))
                print(len(self.x_data))
                

                if(len(self.rssi_data) > len(self.x_data) and self.state == "rssi"):
                    for x in range(len(self.rssi_data)-len(self.x_data)):
                        self.x_data.append(time.time()-self.time_start)
                elif(len(self.rssi_data) < len(self.x_data)):
                    for x in range(len(self.x_data)-len(self.rssi_data)):
                        if(x-1 > 0):
                            self.rssi_data.append(self.rssi_data[x-1])
                        else:
                            self.rssi_data.append(0)

                if(len(self.ultrasonic_data) > len(self.x_data) and self.state == "ultrasonic"):
                    for x in range(len(self.ultrasonic_data)-len(self.x_data)):
                        self.x_data.append(time.time()-self.time_start)
                elif(len(self.ultrasonic_data) < len(self.x_data)):
                    for x in range(len(self.x_data)-len(self.ultrasonic_data)):
                        if(x-1 > 0):
                            self.ultrasonic_data.append(self.ultrasonic_data[x-1])
                        else:
                            self.ultrasonic_data.append(0)
                #relimit the axes
                self.ax.relim()
                #autoscale the axes
                self.ax.autoscale_view(True,True,True)
                #update the axis
                fig.canvas.draw()
                #delay the plot, a annoying but required process
                plt.pause(self.delay)
                time.sleep(self.delay)
            else:
                if(self.graph and self.change):
                    try:
                        self.rssi_data = []
                        self.ultrasonic_data = []
                        plt.close()
                        self.graph = False
                        self.change = False
                    except:
                        print("no plot to close")
                if(not self.graph):
                    rand_color = list(np.random.choice(range(0,100,1), size=3)/100)
                    li, = self.ax.plot(0,0,color = rand_color)
                    self.li_obj = li
                    time_start = time.time()
                    self.x_data = []
                    self.fig = plt.figure()
                    self.ax = fig.add_subplot(111)
                    self.fig.show()
                    self.fig.canvas.draw()
                    plt.show(block=False)
                    plt.pause(self.delay)
                    self.graph = True

class pycom(threading.Thread):
    huzzah = None
    connection = None
    socket = None
    current_state = None
    def __init__(self, huzz, sock, conn):
        threading.Thread.__init__(self)
        self.huzzah = huzz
        self.socket = sock
        self.connection = conn
    def run(self):
        while True:
            if self.huzzah.state != self.current_state:
                self.current_state = self.huzzah.state
            if self.huzzah.state == "menu":
                self.connection.sendall("led gre".encode())
                print("green message sent")
            if self.huzzah.state == "rssi":
                self.connection.sendall("led blu".encode())
                print("blue message sent")
            if self.huzzah.state == "ultrasonic":
                self.connection.sendall("led red".encode())
                print("red message sent")
            
            time.sleep(0.1)
        

class huzzah(threading.Thread):
    plot = None
    state = None
    connection = None
    socket = None
    change = False
    master_state = None
    def __init__(self, plot_obj, sock, conn):
        threading.Thread.__init__(self)
        self.plot = plot_obj
        self.socket = sock
        self.connection = conn
    def run(self):
        print("huzzah loop starting")
        time.sleep(3)
        try:
            self.socket.setblocking(0)
        except:
            traceback.print_exc()
        while True:
            #print("Hello!!!")
            data = None
            try:
                #print("waiting for data")
                data = self.connection.recv(3)
            except:
                pass
            if data is not None:
                data = data.decode()
                self.plot.state = self.state
                print("huzzah state",self.state)
                if self.get_state() == "rssi":
                    self.plot.rssi_data.append(int(data))
                if self.get_state == "ultrasonic":
                    self.plot.ultrasonic_data.append(int(data))
            time.sleep(0.1)
    def get_state(self):
        return self.state
    def send_change(self, c):
        if self.state != c:
            self.change = True
            self.plot.change = True
        if c == "rssi":
            if self.state != "rssi":
                self.plot.state = "rssi"
                self.connection.sendall("rssi".encode())
                print("huzzah, packet sent")
        if c == "ultrasonic":
            if self.state != "ultrasonic":
                self.plot.state = "ultrasonic"
                self.state = "ultrasonic"
                self.connection.sendall("ultr".encode())
                print("huzzah, packet sent")
        if c == "menu":
            if self.state != "menu":
                self.state = "menu"
                self.connection.sendall("menu".encode())
                print("huzzah, packet sent")
        self.state = c
        print("change state",self.state)

        

port = 324
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', port)
sock.bind(server_address)
print("accepting clients on port ",port)
sock.listen(1)
try:
    conn,addr = sock.accept()
except:
    print("???")
plot_obj = plotter()
plot_obj.start()

huzzah_obj = huzzah(plot_obj,sock,conn)
huzzah_obj.start()

print("accepting clients on port ",port)
sock.listen(1)
sock.setblocking(1)
try:
    conn,addr = sock.accept()
except:
    print("???")

pycom_obj = pycom(huzzah_obj,sock,conn)
pycom_obj.start()


state = "menu"
sock.setblocking(0)
while True:
    print("waiting for keypress")
    key_press = ord(msvcrt.getch())
    #r
    if key_press is 114:
        huzzah_obj.send_change("rssi")
    #u    
    elif key_press is 117:
        huzzah_obj.send_change("ultrasonic")
    else:
        huzzah_obj.send_change("menu")
            

