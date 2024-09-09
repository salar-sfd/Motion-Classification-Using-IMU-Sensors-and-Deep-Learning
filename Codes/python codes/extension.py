import bluetooth
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time
import os
import keyboard
import torch
import pickle
import sys

from models import *

class MPU9250(serial.Serial):

    def __init__(self, device_name, ntimesteps=2000, hardware_flag=0, nchannels=6, baudrate=115200, timeout=1):
        self.name = device_name
        self.nchannels = nchannels
        self.ntimesteps = ntimesteps
        self.hardware_flag = hardware_flag
        self.address = MPU9250.find_address(device_name)
        self.data_arr = np.zeros([self.ntimesteps, self.nchannels])
        self.flag_arr = np.zeros(self.ntimesteps)
        self.new_action = 0
        self.action_arr = np.zeros([self.ntimesteps, self.nchannels])
        self.ta = time.time()
        if self.address:
            com_port = MPU9250.discover_port(self.address)
        else:
            print('Bluetooth device not found.')
        super().__init__(port=com_port, baudrate=115200, timeout=1)
        if os.path.exists('settings.pkl'):
            self.load_settings()

    def calibrate(self, ti):
            data_list = []
            print('Calibrating, Keep the Device Still...')
            t0 = time.time()
            while(time.time()-t0 < ti):
                data_list = data_list + self.capture_data_dynamic(0)
            data_list = np.array(data_list)

            self.fs = len(data_list)/ti
            self.data_var = np.var(data_list, axis=0)
            self.gyro_bias = np.mean(data_list[:, 3:6], axis=0)
            self.var_threshold = 6000*self.data_var*0.5
            self.bias_threshold = np.abs(400*self.gyro_bias)*0.5
            self.window_size = int(0.2*self.fs)
            self.save_settings()
            print(f'fs: {self.fs}')

    def save_settings(self, filename='settings.pkl'):
        settings = {
            'fs': self.fs,
            'data_var': self.data_var,
            'gyro_bias': self.gyro_bias,
            'var_threshold': self.var_threshold,
            'bias_threshold': self.bias_threshold,
            'window_size': self.window_size
        }
        
        with open(filename, 'wb') as file:
            pickle.dump(settings, file)
        
        print('Settings saved to', filename)

    def load_settings(self, filename='settings.pkl'):
        with open(filename, 'rb') as f:
            settings = pickle.load(f)
            
            self.fs = settings['fs']
            self.data_var = settings['data_var']
            self.gyro_bias = settings['gyro_bias']
            self.var_threshold = settings['var_threshold']
            self.bias_threshold = settings['bias_threshold']
            self.window_size = settings['window_size']
            
            print('Settings successfully loaded from', filename)

    
    def capture_data(self, gyro_bias=0):
        while True:
            try:
                data = self.readline()[0:-2].decode()
                data = data.split(',')
                data = [float(x) for x in data if x]
                data = np.array(data)
                data[0:3] = data[0:3]/(16384)
                data[3:6] = data[3:6]/(131*180) - gyro_bias
            except:
                print('Sample was Skipped!')
                continue
            if(data.size==self.nchannels+1):
                self.data_arr[0:-1] = self.data_arr[1:]
                self.data_arr[-1] = data[:6]
                self.flag_arr[0:-1] = self.flag_arr[1:]
                self.flag_arr[-1] = self.flag_arr[-2]
            if(self.in_waiting<80):
                break

        if(self.hardware_flag):
            if(self.flag_arr[-1]==1 and data[6]==0):
                self.save_new_action()
            else:
                self.flag_arr[-1] = data[6]

        else:
            if(self.flag_arr[-1]):
                if(np.any(np.var(self.data_arr[-self.window_size:], axis=0)>self.var_threshold*0.1) or np.any(self.data_arr[-self.window_size:, 3:6]>self.bias_threshold*0.1)):
                    self.flag_arr[-1*int(self.window_size):] = 1
                else:
                    self.save_new_action()
            else:
                if(np.any(np.var(self.data_arr[-self.window_size:], axis=0)>self.var_threshold) or np.any(np.mean(np.abs(self.data_arr[-self.window_size:, 3:6]))>self.bias_threshold)):
                    self.flag_arr[-1*int(self.window_size):] = 1
                else:
                    self.flag_arr[-1] = 0
        
        if((self.flag_arr==1).all() and (time.time()-self.ta>=0.5*self.ntimesteps/self.fs)):
            self.save_new_action(filled=True)

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

    def save_new_action(self, filled=False):
        temp = np.where(np.diff(self.flag_arr))[0]
        if(len(temp)):
            action_indx = temp[-1] + 1
        else:
            action_indx = 0
        self.new_action = 1
        self.action_arr = self.action_arr*0
        self.action_arr[:self.ntimesteps-action_indx] = self.data_arr[action_indx:, :]
        self.action_arr[self.ntimesteps-action_indx:] = None
        if(not filled):
            self.flag_arr[-1] = 0
        self.ta = time.time()

    def create_figure(self, figsize=(8, 6)):
        # plt.ion()
        if(figsize == 'full'):
            self.fig, self.axs = plt.subplots(2, 2, figsize=(8, 6))
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
        else:
            self.fig, self.axs = plt.subplots(2, 2, figsize=figsize)
        # plt.show(block=False)

    def update_figure(self, suptitle='IMU'):
        self.fig.suptitle(suptitle)
        for axs in self.axs:
            for ax in axs:
                ax.cla()
        self.axs[0][0].plot(self.data_arr[:, 0:3], label = ['x', 'y', 'z'])
        self.axs[0][0].plot(self.flag_arr, label = 'f')
        self.axs[0][0].set_ylim([-2.5, 2.5])
        self.axs[0][0].set_title('Accelometer')
        self.axs[0][1].plot(self.action_arr[:, 0:3], label = ['x', 'y', 'z'])
        self.axs[0][1].set_ylim([-2.5, 2.5])
        self.axs[0][1].set_title('Accelometer Last Action')
        self.axs[1][0].plot(self.data_arr[:, 3:6], label = ['x', 'y', 'z'])
        self.axs[1][0].plot(self.flag_arr, label = 'f')
        self.axs[1][0].set_ylim([-1.5, 1.5])
        self.axs[1][0].set_title('Gyroscope')
        self.axs[1][1].plot(self.action_arr[:, 3:6], label = ['x', 'y', 'z'])
        self.axs[1][1].set_ylim([-1.5, 1.5])
        self.axs[1][1].set_title('Gyroscope Last Action')

        for axs in self.axs:
            for ax in axs:
                ax.grid(True)
                ax.legend(loc='upper right')

        if(self.flag_arr[-1]):
            self.fig.set_facecolor('red')
        else:
            self.fig.set_facecolor('white')
        plt.draw()
        plt.show(block=False)
        plt.pause(1/1000)

    def dataset_generator(self, dataset_name, ndata=None, class_list=None, method='manual'):
        self.create_figure(figsize='full')
        folder_path = 'Datasets'
        full_path = folder_path+'/'+dataset_name+'.npz'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if os.path.exists(full_path):
            dataset = np.load(full_path)
            x_old = dataset['x']
            y_old = list(dataset['y'])
        if(method == 'manual'):
            x_new = []
            y_new = []
            while True:
                cls = input('Class name (enter -done to finish): ')
                if(cls=='-done'):
                    break
                while not self.new_action:
                    self.capture_data()
                x_new.append(self.action_arr)
                y_new.append(cls)
                self.update_figure()
                self.new_action = 0
            x_new = np.array(x_new)
            plt.pause(0.5)

        if(method == 'automatic'):
            x_new = np.zeros([ndata, self.ntimesteps, self.nchannels])
            y_new = []
            self.update_figure(f'                 Next Class:{class_list[0]}      n = {0}/{ndata}')
            plt.pause(0.5)
            for i in range(ndata):
                cls = class_list[i%len(class_list)]
                while not self.new_action:
                    self.capture_data()
                x_new[i] = self.action_arr
                y_new.append(cls)
                self.update_figure(f'Class: {cls}     Next Class:{class_list[(i+1)%len(class_list)]}      n = {i+1}/{ndata}')
                plt.pause(0.5)
                self.new_action = 0
            
        if os.path.exists(full_path):
            x = np.concatenate([x_old, x_new], axis=0)
            y = y_old + y_new
            np.savez(full_path, x=x, y=y)
            print(f'{len(y_new)} new samples added to previous {len(y_old)} samples. The total number of samples: {len(y)}')
        else:
            np.savez(full_path, x=x_new, y=y_new)
            print(f'{len(y_new)} new samples added. The total number of samples: {len(y_new)}')

    def load_model(self, model_name):
        folder_path = 'Models'
        variables_full_path = folder_path+'/'+model_name+'.pkl'
        model_full_path = folder_path+'/'+model_name+'.pth'
        assert (os.path.exists(model_full_path) and os.path.exists(variables_full_path)), 'Model does not exist.'

        with open(variables_full_path, 'rb') as f:
            data = pickle.load(f)
            preprocessing = data['preprocessing']
            label_encoder = data['label_encoder']
            mean_arr = data['mean_arr']
            std_arr = data['std_arr']

        self.model = globals()[model_name.split('_')[0]](nchannels=self.nchannels, nclasses=len(label_encoder.classes_), preprocessing=preprocessing)        
        self.model.load_state_dict(torch.load(model_full_path))
        self.model.label_encoder = label_encoder
        self.model.mean_arr = mean_arr
        self.model.std_arr = std_arr

    def classify_action(self):
        input = self.action_arr.reshape([1, self.ntimesteps, self.nchannels])
        input = (input-self.model.mean_arr)/self.model.std_arr
        input[np.isnan(input)] = 0
        input = torch.tensor(input.transpose([0, 2, 1]), dtype=torch.float32)
        output = self.model(input)
        _, label = torch.max(output, dim=1)
        self.new_action=0
        return self.model.label_encoder.inverse_transform(label)[0]
    
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