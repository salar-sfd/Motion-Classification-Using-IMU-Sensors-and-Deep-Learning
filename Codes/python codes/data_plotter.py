import time
import numpy as np
import matplotlib.pyplot as plt
from extension import *
import keyboard

te = 100
ti = 2
device_name = 'MPU9250'
buffer_time = 5


# com_port = 'COM13'
box = MPU9250(device_name, buffer_time)
box.initiate(ti)
box.create_figure()

t0 = time.time()
while(time.time()-t0 < te):
    box.capture_data()
    box.update_figure() 
    if keyboard.is_pressed('esc'):
        break
    # print(data_arr[-1]) 
    # print('\r', end='')
    # box.reset_input_buffer()
box.close()
