import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import time
#import numpy 
s = socket.socket()

fig=plt.figure()
rect = fig.patch
rect.set_facecolor("#e0e0e0")
host = "192.168.7.2"
port = 0x8888
pack = 0;
s.connect((host,port))

timepcs = []
ax = []
ay = []
az = []
gx = []
gy = []
gz = []
time.sleep(0.5)
time_template = 'time = %.1fs'
frame_template = 'frame = %.1f'
fps_template = 'fps = %0.1f'

frame = 0
time_start = time.time()

def animate(i):
    xmin = 0
    #s.send("Request from Python")
    '''timepcs = []
    ax = []
    ay = []
    az = []
    gx = []
    gy = []
    gz = []'''
    time_current = time.time() - time_start
    time_text.set_text(time_template%time_current)
    frame_text.set_text(frame_template%i)
    fps_text.set_text(fps_template%i)

    rxbuf = s.recv(1024)
    rx = rxbuf.split('\n')
    #print rx
    for index in range(0,20):
        xAndY = rx[index]
        #print xAndY
        element =xAndY.split(',')
        #print index
        #print timepcs
        if element[0] == '' :
            break
        if float(element[0]) > 3:
            xmin = timepcs.pop(0)
            ax.pop(0)
            ay.pop(0)
            az.pop(0)
            gx.pop(0)
            gy.pop(0)
            gz.pop(0)
        timepcs.append(float(element[0]))
        #print len(timepcs)
        ax.append(int(element[1]))
        ay.append(int(element[2]))
        az.append(int(element[3]))
        gx.append(int(element[4]))
        gy.append(int(element[5]))
        gz.append(int(element[6]))

    ax1.set_xlim(xmin,xmin+3)
    ay1.set_xlim(xmin,xmin+3)
    az1.set_xlim(xmin,xmin+3)
    gx1.set_xlim(xmin,xmin+3)
    gy1.set_xlim(xmin,xmin+3)
    gz1.set_xlim(xmin,xmin+3)

    #s.close()
    ax1.plot(timepcs, ax, 'r')
    ay1.plot(timepcs, ay, 'g')
    az1.plot(timepcs, az, 'b')

    gx1.plot(timepcs, gx, 'r')
    gy1.plot(timepcs, gy, 'g')
    gz1.plot(timepcs, gz, 'b')

    #print timepcs
    '''print ax
    print ay
    print az
    print gx
    print gy
    print gz
    
    ax1.clear()
    ay1.clear()
    az1.clear()
    gx1.clear()
    gy1.clear()
    gz1.clear()'''
    

    
#print timepcs
#print ax
#print ay
#print az
#print gx
#print gy
#print gz
    
ax1 = fig.add_subplot(3,2,1, axisbg='w')
ay1 = fig.add_subplot(3,2,3, axisbg='w')
az1 = fig.add_subplot(3,2,5, axisbg='w')
gx1 = fig.add_subplot(3,2,2, axisbg="gray")
gy1 = fig.add_subplot(3,2,4, axisbg="gray")
gz1 = fig.add_subplot(3,2,6, axisbg="gray")

ax1.set_title('Acce')
gx1.set_title('Gyro')
ax1.set_ylabel('X')
ay1.set_ylabel('Y')
az1.set_ylabel('Z')
az1.set_xlabel('Timepcs (Sec)')
gz1.set_xlabel('Timepcs (Sec)')
    
ax1.set_ylim(-30000,30000)
ay1.set_ylim(-30000,30000)
az1.set_ylim(-30000,30000)
gx1.set_ylim(-40000,40000)
gy1.set_ylim(-40000,40000)
gz1.set_ylim(-40000,40000)

time_text = ax1.text(0.05, 0.81, '', transform=ax1.transAxes)
frame_text = ax1.text(0.05, 0.7, '', transform=ax1.transAxes)
fps_text = ax1.text(0.05, 0.59, '', transform=ax1.transAxes)

    
ani = animation.FuncAnimation(fig, animate, interval=1, blit=False)

plt.show()

