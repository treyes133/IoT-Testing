import sys,socket,time,threading,struct,msvcrt
import numpy as np
import matplotlib.pyplot as plt

class plotter(threading.Thread):
    import matplotlib.pyplot as plt
    import numpy as np
    status = True
    plot_data = []
    plot_data_new = []
    legend = []
    li_list = []
    start_time = time.time()
    delay = 0.1
    x_data = []

    def __init__(self,data):
        threading.Thread.__init__(self)
        self.plot_data = data
    def start(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.show()
        fig.canvas.draw()
        plt.show(block=False)
        time.sleep(1)
        while(self.status is True):
            x_data.append(time.time()-self.start_time)
            ax.legend(legend_list)
            for x in range(0,len(self.plot_data)):
                self.plot_data[x][1].set_xdata(x_data)
                self.plot_data[x][1].set_ydata(self.plot_data[x][2])
            #relimit the axes
            ax.relim()
            #autoscale the axes
            ax.autoscale_view(True,True,True)
            #update the axis
            fig.canvas.draw()
            #delay the plot, a annoying but required process
            plt.pause(delay)

            time.sleep(self.delay)
    def check_changes(self, plot, plot_new):
        plot_merge = []
        new_legend = []
        for x in range(0,len(plot_new)):
            in_list = False
            for stat in plot:
                if plot_new[x][0] is stat[0]:
                    in_list = True
                    plot_merge.append(stat)
                    new_legend.append(stat[0])
                    break
            if not in_list:
                time_change = [0]*((time.time()-self.start_time)/self.delay)
                plot_obj = [[],[],[]]
                rand_color = list(np.random.choice(range(0,100,1), size=3)/100)
                li, = ax.plot(0,0,color = rand_color)
                plot_obj[0] = plot_new[0]
                plot_obj[1] = li
                plot_obj[2].append(time_change)
                plot_obj[2].append(plot_new[1])
                plot_merge.append(plot_obj)
                new_legend.append(plot_obj[0])
        self.plot_data = plot_merge

    def set_plot_data(self,plot):
        self.plot_data_new = plot
        self.check_changes(self.plot_data, self.plot_data_new)
    def stop(self):
        self.status = False

def decompose_header(header):
	destination = header[:header.index(",")]
	header = header[header.index(",")+1:]

	source = header[:header.index(",")]
	header = header[header.index(",")+1:]

	label = header

	return [destination,source,label]
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
def unpack(data,delimiter_sub,delimiter_break):
    data_header = []
    data_labels = []
    data_values = []
    while len(data) > 0:
        data_header.append(data[:data.index(delimiter_sub)])
        data = data[data.index(delimiter_sub)+1:]
        data_labels.append(data[:data.index(delimiter_sub)])
        data = data[data.index(delimiter_sub)+1:]
        data_values.append(data[:data.index(delimiter_break)])
        data = data[data.index(delimiter_break)+1:]
    return [data_header,data_labels,data_values]
def stream_request(sock,source, destination,label,data):
    tag = "stream-request"
    header = str(destination)+","+str(source)+","+str(tag)
    message = header+"+"+str(label)+"+"+str(data)
    print("message type",type(message))
    msg = struct.pack('>I', len(message)).encode('utf-8')+ message
    print(msg)
    sock.sendall(message)

lock = threading.Lock()

#server socket setup (client)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

address = "192.168.4.3"

port = 324
print("hello?")
server_address = (address, port)
print("hello2")
sock.connect(server_address)
print("hello3")
source = "192.168.4.3"

sock.setblocking(0)

rssi = []
ultrasonic = []



try:
    while True:
        print("test1")

        try:
            data = recv_msg(sock)
            [recv_data_headers,recv_data_labels,recv_data_values] = unpack(data,"+",";")
        except:
            #no data
            pass
        try:

            for x in range(0,len(recv_data_headers)):
                header = recv_data_headers[x]
                label = recv_data_labels[x]
                value = recv_data_values[x]
                [dest, source, tag] = decompose_header(header)
                if tag is "stream-data" and value is "rssi":
                    found = False
                    for graphs in rssi:
                        if graphs[0] is source:
                            graphs[1].append(value)
                            found = True
                            break
                    if not found:
                        rssi.append([source,[value]])
                if tag is "stream-data" and value is "ultrasonic":
                    found = False
                    for graphs in ultrasonic:
                        if graphs[0] is source:
                            graphs[1].append(value)
                            found = True
                            break
                    if not found:
                        ultrasonic.append([source,[value]])

        except:
            pass
        key_press = ord(msvcrt.getch())
        if key_press is 114:
            print("Press A to add or R to remove :: ")
            print("Currently Connected")
            print("-------------------")
            for x in range(0,len(rssi)):
                print(x," ",rssi[x][0])
            key_press = ord(msvcrt.getch())
            if(key_press is 97):
                ip = input("Enter IP of rssi client :: ")
                stream_request(sock,source, ip,"rssi","True")
            if(key_press is 114):
                try:
                    num = input("Enter the number to remove :: ")
                    stream_request(sock,source, ip,"rssi","False")
                    del rssi[num]
                except:
                    print("Error, please try again")
        if key_press is 117:
            print("Press A to add or R to remove :: ")
            print("Currently Connected")
            print("-------------------")
            for x in range(0,len(rssi)):
                print(x," ",ultrasonic[x][0])
            key_press = ord(msvcrt.getch())
            if(key_press is 97):
                ip = input("Enter IP of ultrasonic client :: ")
                stream_request(sock,source, ip,"ultrasonic","True")
            if(key_press is 114):
                try:
                    num = input("Enter the number to remove :: ")
                    stream_request(sock,source, ip,"ultrasonic","False")
                    del ultrasonic[num]
                except:
                    print("Error, please try again")
except Exception as e:
    print("Fatal Error ",e)
