import sys,socket,time,threading,_thread
import numpy as np
import matplotlib.pyplot as plt

#lock creation
lock = threading.Lock()

#server socket setup (client)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

address = "192.168.4.1"

port = 324
server_address = (address, port)
sock.connect(server_address)

#some lists to store data
mac_addr = []
rssi = []
mac_list = []
mac_color = []

#our threading exit condition
thread_exit = False
def recv_data(sock):
    #receive 1 byte at a time until a + is received
    #messages are sent TCP by sending information length, followed by +, followed by information
    msglen = ""
    data = sock.recv(1)
    while data is not "+":
        msglen += data
        data = sock.recv(1)
    #might need a conversion here from binary to integer length
    final_data = ""
    data_length = 1024
    #receiving in 1024 bits until the full info is received
    while msglen >= data_length:
        final_data += sock.recv(1024)
        msglen -= data_length
    final_data += sock.recv(msglen)

    #some other lists, these store the new information
    mac_addr = []
    rssi = []
    #move from string to list

    #need to aquire lock to move data around
    lock.aquire()
    while len(final_data) > 0:
        #rip the mac address from the data
        mac_addr.append(final_data[:final_data.index(",")])
        #rip the corresponding rssi from the data
        rssi.append(final_data[final_data.index(",")+1:final_data.index(";")])
        final_data = final_data[final_data.index(";")+1:]
        #check to see if this is a new mac address
        if mac_addr[len(mac_addr)-1] not in mac_list:
            #if so, add it to the list
            mac_list.append(mac_addr[len(mac_addr)-1])
            #create a color for the legend and drawing
            mac_color.append(list(np.random.choice(range(0,100,1), size=3)/100))
    #release the lock, very important!
    lock.release()
            
    return [mac_addr,rssi]
def plotting():
    #global data imports
    global thread_exit
    global lock
    global mac_addr
    global rssi
    global mac_list
    global mac_color

    
    #some initialized variables
    current_reading = 0
    current_macs = 0
    start_time = time.time()
    li_list = []
    legend_list = []
    rssi_data=[]

    #matplotlib starting info
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.show()
    fig.canvas.draw()
    plt.show(block=False)
    
    #system delay
    delay = 0.01

    #not a while true loop, stay away with threads, can cause problems
    while not thread_exit:
        #aquire lock
        lock.aquire()
        #checks if there have been any more added mac addresses
        if(len(mac_list) > current_macs):
            #if so, we need to add them (it is possible to aquire multiple at a time
            for macs in range(current_macs,len(mac_list)-1):
                #create the li object, the list of data, with the color created above
                li, = ax.plot(0,0,color = mac_color[macs])
                #adds to the list
                li_list.append(li)
                #adds the mac address to the legend
                legend_list.append(str(mac_list[macs]))
                #create the rssi_data submatrix
                rssi_data.append([])
            #reset the counter
            current_macs = len(mac_list)
        #updates the legend, if no changes, nothing changes
        ax.legend(legend_list)
        #checks for updates to the list of data
        if(len(mac_addr) > current_reading):
            #same as before, if there was one update, there were probably multiple data entries added
            for reading_position in range(current_reading,len(mac_addr)):
                #add the rssi_data to the corresponding position
                rssi_data[reading_position].append(rssi[reading_position])
            #update the reading variable
            current_reading = len(mac_addr)
        #get system time this will be behind about 10-15ms depending on signal connection, but should be close enough
        current_time = time.time()
        for data_lists in range(0,len(li_list)-1):
            #update the x-data and the y-data for each list
            li_list[data_lists].set_xdata(round(time.time()-current_time,1))
            li_list[data_lists].set_ydata(rssi_data[data_lists])
        #release lock, we are done with shared memory
        lock.release()
        #relimit the axes
        ax.relim()
        #autoscale the axes
        ax.autoscale_view(True,True,True)
        #update the axis
        fig.canvas.draw()
        #delay the plot, a annoying but required process
        plt.pause(delay)
        #sleep for delay seconds, this is what is giving the main thread a chance to update data, might have to be tweaked
        time.sleep(delay)

#create and start the plotting function
_thread.start_new_thread(plotting)
try:
    #run until break
    while True:
        #these are the new mac and rssi data
        [mac_addr_n, rssi_n] = recv_data(sock)
        #add them both to the end of the current data so plotting knows to draw them
        for x in mac_addr_n:
            mac_addr.append(x)
        for y in rssi_n:
            rssi.append(y)
        
finally:
    print("exiting")
