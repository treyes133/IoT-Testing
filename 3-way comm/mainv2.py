import threading,traceback,socket,time,msvcrt
import numpy as np
import matplotlib.pyplot as plt


class plotter(threading.Thread)
    plot_data = []
    x_data = []

    delay = 0.01

    fig = None
    ax = None

    li_objs = []

    time_start = None

    

    def random_color(self):
        return list(np.random.choice(range(0,100,1), size=3)/100)

    def __init__(self, num_plots, names):
        threading.Thread.__init__(self)

        self.fig = plt.figure()
        self.ax = fig.add_subplot(111)

        for x in range(num_plots):
            li, = self.ax.plot(0,0,color = self.rand_color())
            li_objs.append(li)

        self.ax.legend(names)
        
        time_start = time.time()
        self.fig = plt.figure()
        self.ax = fig.add_subplot(111)
        self.fig.show()
        self.fig.canvas.draw()
        plt.show(block=False)
        plt.pause(self.delay)
    def add_values(self, values):
        for x in range(0,len(values)):
            self.plot_data[x].append(values[x])
        self.x_data.append(time.time()-self.time_start)
    def run(self):

        for li_obj in li_objs:
            li_obj.set_xdata(self.x_data)
        for plots in plot_data:
            li_obj.set_ydata(plot)
        
        #relimit the axes
        self.ax.relim()
        #autoscale the axes
        self.ax.autoscale_view(True,True,True)
        #update the axis
        fig.canvas.draw()
        #delay the plot, a annoying but required process
        plt.pause(self.delay)
        time.sleep(self.delay)

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
            

