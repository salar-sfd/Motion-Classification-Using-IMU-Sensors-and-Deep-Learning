import bluetooth
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import time

class MPU9250(serial.Serial):

    def __init__(self, device_name, buffer_time, baudrate=115200, timeout=1):
        self.name = device_name
        self.buffer_time = buffer_time
        self.address = MPU9250.find_address(device_name)
        if self.address:
            com_port = MPU9250.discover_port(self.address)
        else:
            print('Bluetooth device not found.')
        super().__init__(port=com_port, baudrate=115200, timeout=1)

    def initiate(self, ti):
            data_list = []
            print('Initiating...')
            t0 = time.time()
            while(time.time()-t0 < ti):
                data_list = data_list + self.capture_data_dynamic(0)
            data_list = np.array(data_list)
            self.fs = len(data_list)/(time.time()-t0)
            self.data_var = np.var(data_list, axis=0)
            self.gyro_bias = np.mean(data_list[:, 3:6], axis=0)
            self.var_threshold = 4000*self.data_var
            self.bias_threshold = np.abs(300*self.gyro_bias)
            self.window_size = int(0.05*self.fs)
            self.data_length = int(self.buffer_time*self.fs)
            self.data_arr = np.zeros([self.data_length, 6])
            self.flag_arr = np.zeros(self.data_length)
            print('Initiating Done!')

    def capture_data(self, gyro_bias=0):
        while True:
            try:
                data = self.readline()[0:-2].decode()
                data = data.split(',')
                data = [float(x) for x in data if x]
                data = np.array(data[0:-1])
                data[0:3] = data[0:3]/(16384)
                data[3:6] = data[3:6]/(131*180) - gyro_bias
            except:
                print('Sample was skipped!')
                continue
            if(data.size==6):
                self.data_arr[0:-1] = self.data_arr[1:]
                self.data_arr[-1] = data
                self.flag_arr[0:-1] = self.flag_arr[1:]
                self.flag_arr[-1] = self.flag_arr[-2]
            if(self.in_waiting<80):
                break
        if(self.flag_arr[-1]):
            if(np.any(np.var(self.data_arr[-self.window_size:], axis=0)>self.var_threshold*0.7) or np.any(self.data_arr[-self.window_size:, 3:6]>self.bias_threshold*0.7)):
                self.flag_arr[-int(self.window_size):] = 1
            else:
                self.flag_arr[-1] = 0
        else:
            if(np.any(np.var(self.data_arr[-self.window_size:], axis=0)>self.var_threshold) or np.any(np.mean(np.abs(self.data_arr[-self.window_size:, 3:6]))>self.bias_threshold)):
                self.flag_arr[-int(self.window_size):] = 1
            else:
                self.flag_arr[-1] = 0

    def capture_data_dynamic(self, gyro_bias=0):
        data_list = []
        while True:
            try:
                data = self.readline()[0:-2].decode()
                data = data.split(',')
                data = [float(x) for x in data if x]
                data = np.array(data[0:-1])
                data[0:3] = data[0:3]/(16384)
                data[3:6] = data[3:6]/(131*180) - gyro_bias
            except:
                continue
            if(data.size==6):
                data_list.append(data)
            if(self.in_waiting<80):
                break
        return data_list

    def create_figure(self):
        plt.ion()
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8))
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show(block=False)

    def update_figure(self):
        for ax in self.axs:
            ax.cla()

        self.axs[0].plot(self.data_arr[:, 0:3], label = ['x', 'y', 'z'])
        self.axs[1].plot(self.data_arr[:, 3:6], label = ['x', 'y', 'z'])
        self.axs[0].plot(self.flag_arr, label = 'f')
        self.axs[1].plot(self.flag_arr, label = 'f')
        self.axs[0].set_ylim([-2.5, 2.5])
        self.axs[1].set_ylim([-1.5, 1.5])

        for ax in self.axs:
            ax.grid(True)
            ax.legend(loc='upper right')
        if(self.flag_arr[-1]):
            self.fig.set_facecolor('red')
        else:
            self.fig.set_facecolor('white')
        plt.draw()
        plt.pause(1/1000)
         
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