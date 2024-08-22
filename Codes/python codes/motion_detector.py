import serial
import time
import numpy as np
import matplotlib.pyplot as plt

from extension import *

time_limit = 100
spf = 600                                           # sample per frame
device_name = 'MPU9250'

target_address = find_address(device_name)
if target_address:
    com_port = discover_port(target_address)
else:
    print('Bluetooth device not found.')

# com_port = 'COM13'
box = serial.Serial(port=com_port, baudrate=115200, timeout=1)


plt.ion()
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
plt.show(block=False)

data_list = []
n = 0
t0 = time.time()
while(time.time()-t0 < time_limit):
    data_list = data_list + capture_data(box)
    plot_frame(axs, data_list, spf)
    plt.draw()
    plt.pause(1/1000)
    # print(data) 
    # print('\r', end='')
    # box.reset_input_buffer()
    n = n+1
data_list = np.array(data_list)
print(data_list.shape)
print(n)
box.close()
