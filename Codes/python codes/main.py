from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
import threading
import os
import time
from extension import *



class Application(BoxLayout):

    def __init__(self, obj, tc, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj
        self.tc = tc
        self.orientation = 'vertical'
        self.button_bg = [0.04, 0.18, 0.30, 1]
        self.button_fg = [1, 1, 1, 1]
        self.create_main_menu()

    def clear_window(self):
        self.clear_widgets()

    def create_main_menu(self):
        self.clear_window()

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)

        classify_button = Button(text='Classify', size_hint_y=None, height=50, background_color=self.button_bg)
        classify_button.bind(on_press=self.select_model)
        layout.add_widget(classify_button)

        calibrate_button = Button(text='Calibrate', size_hint_y=None, height=50, background_color=self.button_bg)
        calibrate_button.bind(on_press=self.calibrate)
        layout.add_widget(calibrate_button)

        plot_button = Button(text='Plot Data', size_hint_y=None, height=50, background_color=self.button_bg)
        plot_button.bind(on_press=self.plot_data)
        layout.add_widget(plot_button)

        dataset_button = Button(text='Modify Datasets', size_hint_y=None, height=50, background_color=self.button_bg)
        dataset_button.bind(on_press=self.select_dataset)
        layout.add_widget(dataset_button)

        motion_text = 'Motion Detection: ' + ('Hardware' if self.obj.hardware_flag else 'Software')
        motion_detection_button = Button(text=motion_text, size_hint_y=None, height=50, background_color=[0.12, 0.37, 0.13, 1] if self.obj.hardware_flag else [0.36, 0, 0.13, 1])
        motion_detection_button.bind(on_press=self.swap_flag)
        layout.add_widget(motion_detection_button)

        quit_button = Button(text='Quit', size_hint_y=None, height=50, background_color=[0.02, 0.10, 0.19, 1])
        quit_button.bind(on_press=self.quit_app)
        layout.add_widget(quit_button)

    def plot_data(self, instance):
        self.clear_window()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)

        fig, axs = plt.subplots(2, 2)
        canvas = FigureCanvasKivyAgg(fig)
        layout.add_widget(canvas)

        self.updating = True
        Clock.schedule_interval(lambda dt: self.update_plot(axs, canvas), 1)

        return_button = Button(text="Return", size_hint_y=None, height=50, background_color=self.button_bg)
        return_button.bind(on_press=self.return_to_main_menu)
        layout.add_widget(return_button)

    def update_plot(self, axs, canvas):
        if self.updating:
            self.obj.capture_data()
            axs[0][0].cla()
            axs[0][0].plot(self.obj.data_arr[:, 0:3])
            axs[0][1].cla()
            axs[0][1].plot(self.obj.action_arr[:, 0:3])
            axs[1][0].cla()
            axs[1][0].plot(self.obj.data_arr[:, 3:6])
            axs[1][1].cla()
            axs[1][1].plot(self.obj.action_arr[:, 3:6])
            canvas.draw()

    def calibrate(self, instance):
        self.clear_window()
        label = Label(text="Calibrating...", size_hint_y=None, height=50)
        self.add_widget(label)

        threading.Thread(target=self.run_calibration).start()

    def run_calibration(self):
        self.obj.calibrate(self.tc)
        self.create_main_menu()

    def select_model(self, instance):
        self.clear_window()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)

        model_directory = 'Models'
        try:
            model_names = [os.path.splitext(f)[0] for f in os.listdir(model_directory) if os.path.isfile(os.path.join(model_directory, f))]
        except FileNotFoundError:
            model_names = []

        for model_name in model_names:
            btn = Button(text=model_name, size_hint_y=None, height=50, background_color=self.button_bg)
            btn.bind(on_press=lambda x, model=model_name: self.classify(model))
            layout.add_widget(btn)

        return_button = Button(text="Return", size_hint_y=None, height=50, background_color=self.button_bg)
        return_button.bind(on_press=self.create_main_menu)
        layout.add_widget(return_button)

    def classify(self, model_name):
        self.clear_window()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)

        self.obj.load_model(model_name)
        self.obj.model.eval()

        self.text_screen = TextInput(multiline=True, readonly=True, size_hint_y=None, height=300)
        layout.add_widget(self.text_screen)

        self.updating = True
        Clock.schedule_interval(lambda dt: self.capture_and_classify(), 1)

        return_button = Button(text="Return", size_hint_y=None, height=50, background_color=self.button_bg)
        return_button.bind(on_press=self.return_to_main_menu)
        layout.add_widget(return_button)

    def capture_and_classify(self):
        if self.updating:
            self.obj.capture_data()
            if self.obj.new_action:
                label = self.obj.classify_action()
                if label == "\\n":
                    label = "\n"
                elif label == "\\b":
                    self.text_screen.delete_text(self.text_screen.text[:-1])
                else:
                    self.text_screen.insert_text(label)

    def select_dataset(self, instance):
        self.clear_window()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)

        dataset_directory = 'Datasets'
        try:
            dataset_names = [os.path.splitext(f)[0] for f in os.listdir(dataset_directory) if os.path.isfile(os.path.join(dataset_directory, f))]
        except FileNotFoundError:
            dataset_names = []

        for dataset_name in dataset_names:
            btn = Button(text=dataset_name, size_hint_y=None, height=50, background_color=self.button_bg)
            btn.bind(on_press=lambda x, dataset=dataset_name: self.helper_func(dataset))
            layout.add_widget(btn)

        return_button = Button(text="Return", size_hint_y=None, height=50, background_color=self.button_bg)
        return_button.bind(on_press=self.return_to_main_menu)
        layout.add_widget(return_button)

    def helper_func(self, dataset_name):
        # Implementation of dataset modification logic
        pass

    def swap_flag(self, instance):
        self.obj.hardware_flag = not self.obj.hardware_flag
        self.create_main_menu()

    def return_to_main_menu(self, instance):
        self.updating = False
        self.create_main_menu()

    def quit_app(self, instance):
        self.obj.close()
        App.get_running_app().stop()


class MyApp(App):
    def build(self):
        tc = 3
        device_name = 'MPU9250'
        box = MPU9250(device_name, hardware_flag=False, ntimesteps=2048)
        return Application(obj=box, tc=tc)


if __name__ == '__main__':
    MyApp().run()
