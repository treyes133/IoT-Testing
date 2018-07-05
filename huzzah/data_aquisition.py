import sys,socket,time,machine,network,threading,struct
from machine import Pin, Signal

class rssi_thread(threading.Thread):
    self.status = True
    self.sta_if = None
    #sample rate is per second
    self.sample = 10
    self.rssi_value = None

    def __init__(self,sta_if_obj):
        threading.Thread.__init__(self)
        self.sta_if = sta_if_obj
    def start(self):
        while(self.status is True):
            self.rssi_value = sta_if.status("rssi")
            time.sleep(1/self.sample)
    def set_rate(self,rate):
        self.sample = rate
    def get_rssi(self):
        return self.rssi_value
    def stop(self):
        self.status = False



services = ["rssi","led","gpio"]


sta_if = network.WLAN(network.STA_IF)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_address = "192.168.4.2_Huzzah"


address = "192.168.4.1"
port = 324

server_address = (address, port)

sock.connect(server_address)
socket.setblocking(0)

rssi = False
rssi_status_change = False
rssi_t = rssi_thread(sta_if)

led_status = False
gpio = []
recv_data_labels = []
recv_data_values = []

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
try:
    while True:
        try:
            data = recv_msg(sock)
            [recv_data_headers,recv_data_labels,recv_data_values] = unpack(data,"+",";")
        except:
            #no data
            pass

        #update status
        try:

            for x in range(0,len(recv_data_headers)):
                header = recv_data_headers[x]
                label = recv_data_labels[x]
                value = recv_data_values[x]
                [dest, source, tag] = decompose_header(header)
                if tag is "stream-request" and value is "rssi":
                    if(value is True and rssi is False):
                        rssi = True
                        rssi_status_change = True
                    if(value is False and rssi is True):
                        rssi = False
                        rssi_status_change = True
        except:
            pass

        #clear received data
        [recv_data_headers,recv_data_labels,recv_data_values] = None

        #change variables
        if(rssi_status_change):
            rssi_status_change = False
            if(rssi is True):
                rssi_t.start()
            if(rssi is False)
                rssi_t.stop()

        #send data
        message = ""
        if(rssi):
            rssi_value = rssi_t.get_rssi()
            header = "server"+","+str(client_address)+",stream-data"
            label = "rssi"
            message += header+"+"+label+"+"+str(rssi_value)+";"
        if(message is not None):
            msg = struct.pack(">I", len(message)) + message
            sock.sendall(msg)
