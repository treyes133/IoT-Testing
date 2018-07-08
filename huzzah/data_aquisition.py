import socket, utime
import machine, network
import ustruct

from machine import Pin

echo = machine.Pin(14,machine.Pin.IN)
trig = machine.Pin(12,machine.Pin.OUT)

trig.off()
utime.sleep(3)

class rssi_thread:
    status = True
    sta_if = None
    #sample rate is per second
    sample = 10
    rssi_value = None

    def __init__(self,sta_if_obj):
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


class ultrasonic_thread:
    status = True
    #sample rate is per second
    sample = 10
    average = 4
    ultrasonic_value = None

    def __init__(self):
        pass
    def start(self):
        while(self.status is True):
            self.ultrasonic_value = measurement(self.average)
            time.sleep(1/self.sample)
    def set_rate(self,rate):
        self.sample = rate
    def get_ultrasonic(self):
        return self.ultrasonic_value
    def stop(self):
        self.status = False


print("STARTING")
services = ["rssi","led","gpio"]


sta_if = network.WLAN(network.STA_IF)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_address = "192.168.4.2"


address = "192.168.4.3"
port = 324

server_address = (address, port)

sock.connect(server_address)
print("TEST2")
sock.setblocking(0)

rssi = False

ultra = False


led_status = False
gpio = []
recv_data_headers = []
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
def measurement(avg):

    global echo
    global trig
    measurements = []
    for x in range(0,avg+1):
        trig.on()
        utime.sleep_us(10)
        trig.off()
        pulse_start=0
        pulse_end=0
        timeout = 10000
        while echo.value() is 0 and timeout > 0:
            pulse_start = utime.ticks_us()
            timeout -= 1

        timeout = 10000
        while echo.value() is 1 and timeout > 0:
            pulse_end = utime.ticks_us()
            timeout -=1
        if timeout > 0:
            pulse_duration = utime.ticks_diff(pulse_end,pulse_start)/(pow(10,6))
            distance = pulse_duration * 17150

            distance = round(distance, 2)
            measurements.append(distance)
        else:
            measurements.append(0)


    utime.sleep_us(10)
    return sum(measurements)/len(measurements)
try:
    print("starting")
    while True:
        try:
            data = recv_msg(sock)
            [recv_data_headers,recv_data_labels,recv_data_values] = unpack(data,"+",";")
        except:
            print("no data")

        #update status
        try:
            print("TEST3")
            if(len(recv_data_headers) is not 0):
                for x in range(0,len(recv_data_headers)):
                    header = recv_data_headers[x]
                    label = recv_data_labels[x]
                    value = recv_data_values[x]
                    [dest, source, tag] = decompose_header(header)
                    if tag is "stream-request" and value is "rssi":
                        if(value is True and rssi is False):
                            rssi = True
                        if(value is False and rssi is True):
                            rssi = False
                    if tag is "stream-request" and value is "ultrasonic":
                        if(value is True and ultra is False):
                            ultra = True
                        if(value is False and ultra is True):
                            ultra = False

        except:
            pass

        #clear received data
        recv_data_headers = None
        recv_data_labels = None
        recv_data_values = None

        print("TEST4")
        #send data
        message = ""
        if(rssi):
            rssi_value = sta_if.status("rssi")
            header = "server"+","+client_address+",stream-data"
            label = "rssi"
            message += header+"+"+label+"+"+str(rssi_value)+";"
        if(ultra):
            ultra_value = measurement(4)
            header = "server"+","+client_address+",stream-data"
            label = "ultrasonic"
            message += header+"+"+label+"+"+str(ultra_value)+";"
        if(len(message) > 0):
            msg = struct.pack('>I', len(message)) + message
            sock.sendall(msg)
except Exception as exp:
    print("Exiting ",exp)
