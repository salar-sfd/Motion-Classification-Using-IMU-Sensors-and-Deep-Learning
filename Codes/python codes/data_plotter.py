import time
import keyboard
from extension import *

te = 200
ti = 3
device_name = 'MPU9250'

box = MPU9250(device_name, hardware_flag=True, ntimesteps=2048)
box.initiate(ti)
box.create_figure()

# t0 = time.time()
# while(time.time()-t0 < te):
#     box.capture_data()
#     box.update_figure() 
#     if keyboard.is_pressed('esc'):
#         break
#     # print(box.data_arr[-1, :]) 
#     # print('\r', end='')
#     # box.reset_input_buffer()

# class_list = ['a','b','c', 'd', 'e']
# box.dataset_generator('alphabet1', len(class_list)*3, class_list, method='automatic')

box.load_model('AirNet')
box.model.eval()
t0 = time.time()
while (time.time()-t0 < te):
    box.capture_data()
    if(box.new_action==1):
        box.classify_action()
    if keyboard.is_pressed('esc'):
        break

box.close()
