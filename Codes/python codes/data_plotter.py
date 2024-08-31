import time
import keyboard
from extension import *

te = 200
tc = 3
device_name = 'MPU9250'

box = MPU9250(device_name, hardware_flag=False, ntimesteps=2048)
box.calibrate(tc)

# box.create_figure()
# t0 = time.time()
# while(time.time()-t0 < te):
#     box.capture_data()
#     box.update_figure() 
#     if keyboard.is_pressed('esc'):
#         break
    # print(box.flag_arr[-1]) 
    # print('\r', end='')
    # box.reset_input_buffer()

class_list = ['a','b','c', 'd', 'e']
box.dataset_generator('alphabet', len(class_list)*3, class_list, method='automatic')

# box.load_model('AirNet')
# box.model.eval()
# t0 = time.time()
# while (time.time()-t0 < te):
#     box.capture_data()
#     if(box.new_action==1):
#         label = box.classify_action()
#         print(label, end='')
#         sys.stdout.flush()
#     if keyboard.is_pressed('esc'):
#         break

box.close()
