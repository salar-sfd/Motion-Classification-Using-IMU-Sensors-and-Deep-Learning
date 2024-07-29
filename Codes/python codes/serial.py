import serial
import time
import numpy as np
import matplotlib.pyplot as plt
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=1)
data_list = []
n=0
t0 = time.time()
plt.show(block=False)
while time.time()-t0 < 50:
    t1 = time.time()
    data = arduino.readline()[0:-2].decode()
    try:
        data = data.split(',')
        data = [float(x) for x in data if x]
        if(data):
            if(len(data)==6 and np.sum(data)<10):
                data_list.append(data)
                # plt.clf()
                # if(len(data_list)>200):
                #     plt.plot(np.array(data_list)[-200:-1])
                # else:
                #     plt.plot(np.array(data_list))
                # plt.draw()
                # plt.pause(0.00001)
    except:
        pass
    print(data) 
    arduino.reset_input_buffer()
    print('\r', end='')

data_list = np.array(data_list)
print(data_list.shape)

arduino.close()
