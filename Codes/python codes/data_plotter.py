import serial
import time
import numpy as np
import matplotlib.pyplot as plt

from extension import *

te = 100
ti = 2
spf = 600                                           # sample per frame
device_name = 'MPU9250'

target_address = find_address(device_name)
if target_address:
    com_port = discover_port(target_address)
else:
    print('Bluetooth device not found.')

# com_port = 'COM13'
box = serial.Serial(port=com_port, baudrate=115200, timeout=1)
fs, data_var, gyro_bias = calibrate(box, ti)

threshold_rise = 5000
threshold_fall = 800
threshold = threshold_rise*data_var
window_size = int(0.1*fs)
flag_list = [0]

plt.ion()
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
plt.show(block=False)

data_list = []
t0 = time.time()
while(time.time()-t0 < te):
    data_list = data_list + capture_data(box, gyro_bias)
    plot_frame(axs, data_list, flag_list[-1], spf)
    


    if(np.any(np.var(np.array(data_list[-window_size:-1]), axis=0)>threshold)):
        flag_list = [flag_list, 1]
        threshold = threshold_fall*data_var
    else:
        flag_list = [flag_list, 0]
        threshold = threshold_rise*data_var
    
    
    # print(data_list[-1]) 
    # print('\r', end='')
    # box.reset_input_buffer()
data_list = np.array(data_list)
print(data_list.shape)
box.close()
