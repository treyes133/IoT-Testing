import matplotlib.pyplot as plt
import numpy as np
import time

start_time = time.time()
x_dat = [0]
y_dat = list(np.random.choice(range(-100,-10,1), size=1000))
y_dat2 = list(np.random.choice(range(-100,-10,1), size=1000))

fig = plt.figure()
ax = fig.add_subplot(111)

fig.show()
fig.canvas.draw()

li, = ax.plot(0,0,color = (0.1,0.5,1))
li2, = ax.plot(0,0,color = (0.3,0,1))
x = [0]
y = [-50]
y2 = [-40]
t = 0
delay = 0.001
ax.legend(["L1","L2"])
plt.show(block=False)
for a in range(1,len(y_dat)):
    x.append(x_dat[t])
    y.append(y_dat[t])
    y2.append(y_dat2[t])
    li.set_xdata(x)
    li.set_ydata(y)
    li2.set_xdata(x)
    li2.set_ydata(y2)
    time.sleep(0.01)
    x_dat.append(time.time()-start_time)
    t += 1
    ax.relim() 
    ax.autoscale_view(True,True,True) 

    fig.canvas.draw()
    plt.pause(0.001)

