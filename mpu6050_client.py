import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket 
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
   
def animate(i):
    #s.send("Request from Python")
    '''timepcs = []
    ax = []
    ay = []
    az = []
    gx = []
    gy = []
    gz = []'''
    for rxbuf_index in range(0,500):
        rxbuf = s.recv(64)
        rx = rxbuf.split('\n')      
        xAndY = rx[0].split(',')
        #print xAndY[0]
        if xAndY[0] == '' :
            break
        timepcs.append(float(xAndY[0]))
        ax.append(int(xAndY[1]))
        ay.append(int(xAndY[2]))
        az.append(int(xAndY[3]))
        gx.append(int(xAndY[4]))
        gy.append(int(xAndY[5]))
        gz.append(int(xAndY[6]))

    #s.close()

    '''print timepcs
    print ax
    print ay
    print az
    print gx
    print gy
    print gz'''
    
    ax1.clear()
    ay1.clear()
    az1.clear()
    gx1.clear()
    gy1.clear()
    gz1.clear()
    
    ax1.set_title('Acce')
    gx1.set_title('Gyro')
    ax1.set_ylabel('X')
    ay1.set_ylabel('Y')
    az1.set_ylabel('Z')
    az1.set_xlabel('Timepcs (Sec)')
    gz1.set_xlabel('Timepcs (Sec)')
    
    ax1.plot(timepcs, ax, 'r')
    ay1.plot(timepcs, ay, 'g')
    az1.plot(timepcs, az, 'b')

    gx1.plot(timepcs, gx, 'r')
    gy1.plot(timepcs, gy, 'g')
    gz1.plot(timepcs, gz, 'b')

    '''ax1.set_xlim(0,1)
    ay1.set_xlim(0,1)
    az1.set_xlim(0,1)
    gx1.set_xlim(0,1)
    gy1.set_xlim(0,1)
    gz1.set_xlim(0,1)'''

    ax1.set_ylim(-40000,40000)
    ay1.set_ylim(-40000,40000)
    az1.set_ylim(-40000,40000)
    gx1.set_ylim(-40000,40000)
    gy1.set_ylim(-40000,40000)
    gz1.set_ylim(-40000,40000)
    
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

ani = animation.FuncAnimation(fig, animate, interval=10)

plt.show()

