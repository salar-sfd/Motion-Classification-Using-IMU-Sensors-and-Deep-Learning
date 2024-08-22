import bluetooth
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import time

def find_address(device_name):
    print("Scanning for Bluetooth devices...")
    devices = bluetooth.discover_devices(duration=1, lookup_names=True, flush_cache=True, lookup_class=False)
    target_address = None
    for addr, name in devices:
        if name == device_name:
            target_address = addr
            print(f'Found device {name}')
            break
    return target_address

def discover_port(device_address):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if device_address.replace(":", "").upper() in port.hwid.upper():
            return port.device
    return None

def capture_data(box, gyro_bias):
    data_list = []
    while True:
        data = box.readline()[0:-2].decode()
        data = data.split(',')
        data = [float(x) for x in data if x]
        data = np.array(data[0:-1])
        data[0:3] = data[0:3]/(16384)
        data[3:6] = data[3:6]/(131*180) - gyro_bias
        if(data.size==6):
            data_list.append(data)
        if(box.in_waiting<80):
            break
    return data_list

def plot_frame(axs, data_list, flag, spf):
    fig = plt.gcf()
    for ax in axs:
        ax.cla()
    if(len(data_list) > spf):
        axs[0].plot(np.array(data_list[-spf:-1])[:, 0:3], label = ['x', 'y', 'z'])
        axs[1].plot(np.array(data_list[-spf:-1])[:, 3:6], label = ['x', 'y', 'z'])
    else:
        axs[0].plot(np.array(data_list)[:, 0:3], label = ['x', 'y', 'z'])
        axs[1].plot(np.array(data_list)[:, 3:6], label = ['x', 'y', 'z'])
    for ax in axs:
        ax.grid(True)
        ax.set_ylim([-2, 2])
        ax.legend(loc='upper right')
    if(flag):
        fig.set_facecolor('red')
    else:
        fig.set_facecolor('lightblue')
    plt.draw()
    plt.pause(1/1000)

def calibrate(box, ti):
    data_list = []
    print('Calibrating...')
    t0 = time.time()
    while(time.time()-t0 < ti):
        data_list = data_list + capture_data(box, 0)
    fs = len(data_list)/(time.time()-t0)
    data_list = np.array(data_list)

    data_var = np.var(data_list, axis=0)
    gyro_bias = np.mean(data_list[:, 3:6], axis=0)
    print('Calibration Done!')
    return fs, data_var, gyro_bias

# def motion_detector(fs):
    # window_size = np.floor(0.1*fs)
    # thre_rise = 5000
    # thre_fall = 800
    # if(np.any(var([accel_list(end-window_size+1:end, :), gyro_list(end-window_size+1:end, :)])>threshold))
    #     disp(1);
    #     flag_list = [flag_list, 1];
    #     threshold = threshold_fall*[accel_var, gyro_var];
    # else
    #     disp(0);
    #     flag_list = [flag_list, 0];
    #     threshold = threshold_rise*[accel_var, gyro_var];
    # end
