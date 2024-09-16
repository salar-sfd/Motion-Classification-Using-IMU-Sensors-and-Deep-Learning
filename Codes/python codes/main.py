from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.core.window import Window

import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import os

from extension import MPU9250

class IMUApp(App):
    def __init__(self, obj, tc, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj
        self.tc = tc
        self.updating = False
        self.update_interval = 1
        self.buttons = []
        self.textboxes = []
        self.entries = []

    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.create_main_menu()
        return self.root

    def create_main_menu(self):
        self.clear_window()
        
        classify_button = Button(text='Classify', on_press=self.select_model)
        calibrate_button = Button(text='Calibrate', on_press=self.calibrate)
        plot_button = Button(text='Plot Data', on_press=self.plot_data)
        dataset_creator_button = Button(text='Modify Datasets', on_press=self.select_dataset)
        
        motion_text = 'Motion Detection: ' + ('Hardware' if self.obj.hardware_flag else 'Software')
        motion_detection_button = Button(text=motion_text, on_press=self.swap_flag,
                                         background_color=(0.07, 0.37, 0.16, 1) if self.obj.hardware_flag else (0.36, 0, 0.05, 1))
        
        quit_button = Button(text='Quit', on_press=self.quit_app, background_color=(0.02, 0.1, 0.19, 1))

        self.buttons = [classify_button, calibrate_button, plot_button, dataset_creator_button, motion_detection_button, quit_button]
        
        for button in self.buttons:
            self.root.add_widget(button)

    def clear_window(self):
        self.root.clear_widgets()

    def plot_data(self, instance):
        self.clear_window()

        self.fig, self.axs = plt.subplots(2, 2, figsize=(10, 8))
        self.canvas = FigureCanvasKivyAgg(self.fig)
        self.root.add_widget(self.canvas)

        return_button = Button(text='Return', on_press=self.return_to_main_menu, size_hint=(1, 0.1))
        self.root.add_widget(return_button)

        self.updating = True
        Clock.schedule_interval(self.capture_and_plot, self.update_interval / 1000.0)

    def return_to_main_menu(self, instance):
        self.updating = False
        Clock.unschedule(self.capture_and_plot)
        self.create_main_menu()

    def capture_and_plot(self, dt):
        if self.updating:
            self.obj.capture_data()
            self.update_figure()
            self.canvas.draw()

    def calibrate(self, instance):
        self.clear_window()

        label = Label(text='Calibrating...', size_hint=(1, 0.9))
        self.root.add_widget(label)

        def calibrate_and_return():
            self.obj.calibrate(self.tc)
            Clock.schedule_once(lambda dt: self.create_main_menu(), 0)

        threading.Thread(target=calibrate_and_return).start()

    def select_model(self, instance):
        self.clear_window()

        model_directory = 'Models'
        try:
            model_names = [os.path.splitext(f)[0] for f in os.listdir(model_directory) if os.path.isfile(os.path.join(model_directory, f))]
        except FileNotFoundError:
            print('Model directory not found.')
            model_names = []
        model_names = list(set(model_names))
        
        for model_name in model_names:
            button = Button(text=model_name, on_press=lambda x, name=model_name: self.classify(name))
            self.root.add_widget(button)
        
        return_button = Button(text='Return', on_press=self.create_main_menu, background_color=(0.02, 0.1, 0.19, 1))
        self.root.add_widget(return_button)

    def classify(self, model_name):
        self.clear_window()

        self.text_screen = TextInput(text='', multiline=True, size_hint=(1, 0.8))
        self.root.add_widget(self.text_screen)

        return_button = Button(text='Return', on_press=self.create_main_menu, size_hint=(1, 0.2))
        self.root.add_widget(return_button)

        self.model_name = model_name
        self.obj.load_model(model_name)
        self.obj.model.eval()

        self.updating = True
        Clock.schedule_interval(self.capture_and_classify, self.update_interval / 1000.0)

    def capture_and_classify(self, dt):
        if self.updating:
            self.obj.capture_data()
            if self.obj.new_action:
                label = self.obj.classify_action()
                label = '\n' if label=='\\n' else '\b' if label=='\\b' else ' ' if label=='\s' else label
                if len(label) > 1:
                    self.text_screen.text = ''
                if label == '\b':
                    self.text_screen.text = self.text_screen.text[:-1]
                else:
                    self.text_screen.text += label

    def select_dataset(self, instance):
        self.clear_window()

        self.text_screen1 = TextInput(text='Classes Separated by Space:', multiline=False, size_hint=(1, 0.1))
        self.root.add_widget(self.text_screen1)

        self.entry = TextInput(text='', multiline=False, size_hint=(0.8, 0.1))
        self.root.add_widget(self.entry)
        new_button = Button(text='Create New', on_press=lambda x: self.helper_func(self.entry.text), size_hint=(0.2, 0.1))
        self.root.add_widget(new_button)

        dataset_directory = 'Datasets'
        try:
            dataset_names = [os.path.splitext(f)[0] for f in os.listdir(dataset_directory) if os.path.isfile(os.path.join(dataset_directory, f))]
        except FileNotFoundError:
            print('Dataset directory not found.')
            dataset_names = []
        dataset_names = list(set(dataset_names))

        for dataset_name in dataset_names:
            button = Button(text=dataset_name, on_press=lambda x, name=dataset_name: self.helper_func(name))
            self.root.add_widget(button)

        return_button = Button(text='Return', on_press=self.return_to_main_menu, background_color=(0.02, 0.1, 0.19, 1))
        self.root.add_widget(return_button)

    def helper_func(self, dataset_name):
        class_list = self.text_screen1.text.strip().split()
        self.dataset_name = dataset_name
        self.class_list = class_list
        self.modify_dataset()

    def modify_dataset(self):
        self.clear_window()

        self.fig, self.axs = plt.subplots(2, 2, figsize=(10, 8))
        self.canvas = FigureCanvasKivyAgg(self.fig)
        self.root.add_widget(self.canvas)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.cancel_button = Button(text='Cancel', on_press=self.return_to_select_dataset)
        self.delete_button = Button(text='Delete Last', on_press=self.delete_last_action)
        self.save_button = Button(text='Save', on_press=self.save_dataset)

        button_layout.add_widget(self.cancel_button)
        button_layout.add_widget(self.delete_button)
        button_layout.add_widget(self.save_button)

        self.root.add_widget(button_layout)

        self.updating = True
        self.x_new = []
        self.y_new = []
        self.n = 0
        self.update_figure(f'                 Next Class:{self.class_list[0]}      n = {0}')
        self.canvas.draw()
        Clock.schedule_interval(self.capture_and_create, self.update_interval / 1000.0)

    def capture_and_create(self, dt):
        if self.updating:
            self.obj.capture_data()
            if self.obj.new_action:
                cls = self.class_list[(self.n) % len(self.class_list)]
                self.x_new.append(self.obj.action_arr)
                self.y_new.append(cls)
                self.update_figure(f'Class: {cls}     Next Class: {self.class_list[(self.n+1)%len(self.class_list)]}      n = {self.n+1}')
                self.canvas.draw()

                self.obj.new_action = 0
                self.n += 1

    def delete_last_action(self, instance):
        if self.n == 0:
            return
        
        self.x_new.pop(-1)
        self.y_new.pop(-1)
        self.obj.action_arr = self.obj.action_arr * 0 if self.n == 1 else self.x_new[-1]
        self.obj.new_action = 0
        self.n -= 1
        
        self.update_figure(f'Class: {self.class_list[(self.n-1)%len(self.class_list)]}     Next Class: {self.class_list[(self.n)%len(self.class_list)]}      n = {self.n}')
        self.canvas.draw()

    def save_dataset(self, instance):
        self.clear_window()
        self.updating = False
        Clock.unschedule(self.capture_and_create)
        
        folder_path = 'Datasets'
        full_path = folder_path + '/' + self.dataset_name + '.npz'
        self.x_new = np.array(self.x_new)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if os.path.exists(full_path):
            dataset = np.load(full_path)
            x_old = dataset['x']
            y_old = list(dataset['y'])

        if os.path.exists(full_path):
            x = np.concatenate([x_old, self.x_new], axis=0)
            y = y_old + self.y_new
            np.savez(full_path, x=x, y=y)
            text = f'{len(self.y_new)} new samples added to previous {len(y_old)} samples. The total number of samples: {len(y)}'
        else:
            np.savez(full_path, x=self.x_new, y=self.y_new)
            text = f'{len(self.y_new)} new samples added. The total number of samples: {len(self.y_new)}'

        label = Label(text=text)
        self.root.add_widget(label)

        Clock.schedule_once(lambda dt: self.select_dataset(None), 2)

    def swap_flag(self, instance):
        self.obj.hardware_flag = not self.obj.hardware_flag
        self.create_main_menu()

    def update_figure(self, suptitle='IMU'):
        self.fig.suptitle(suptitle)
        for axs in self.axs:
            for ax in axs:
                ax.cla()
        self.axs[0][0].plot(self.obj.data_arr[:, 0:3], label=['x', 'y', 'z'])
        self.axs[0][0].plot(self.obj.flag_arr, label='f')
        self.axs[0][0].set_ylim([-2.5, 2.5])
        self.axs[0][0].set_title('Accelerometer')
        self.axs[0][1].plot(self.obj.action_arr[:, 0:3], label=['x', 'y', 'z'])
        self.axs[0][1].set_ylim([-2.5, 2.5])
        self.axs[0][1].set_title('Accelerometer Last Action')
        self.axs[1][0].plot(self.obj.data_arr[:, 3:6], label=['x', 'y', 'z'])
        self.axs[1][0].plot(self.obj.flag_arr, label='f')
        self.axs[1][0].set_ylim([-1.5, 1.5])
        self.axs[1][0].set_title('Gyroscope')
        self.axs[1][1].plot(self.obj.action_arr[:, 3:6], label=['x', 'y', 'z'])
        self.axs[1][1].set_ylim([-1.5, 1.5])
        self.axs[1][1].set_title('Gyroscope Last Action')

        for axs in self.axs:
            for ax in axs:
                ax.grid(True)
                ax.legend(loc='upper right')

        if self.obj.flag_arr[-1]:
            self.fig.patch.set_facecolor('red')
        else:
            self.fig.patch.set_facecolor('white')

    def quit_app(self, instance):
        self.obj.close()
        App.get_running_app().stop()
        Window.close()

if __name__ == '__main__':
    tc = 3
    device_name = 'MPU9250'
    box = MPU9250(device_name, hardware_flag=False, ntimesteps=2048)
    IMUApp(obj=box, tc=tc).run()
    os._exit(0)