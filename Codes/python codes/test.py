import tkinter as tk
from tkinter import messagebox
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from extension import *

class Application(tk.Tk):
    def __init__(self, obj, tc):
        super().__init__()
        self.obj = obj
        self.tc = tc
        self.title("Main Menu")
        self.geometry("600x500")  # Adjusted to accommodate the plot and buttons
        # Main Menu Buttons
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        plot_button = tk.Button(self, text="Plot Data", command=self.data_plot)
        plot_button.pack(pady=10)

        calibrate_button = tk.Button(self, text="Calibrate", command=self.calibrate)
        calibrate_button.pack(pady=10)

        classify_button = tk.Button(self, text="Classify", command=self.classify)
        classify_button.pack(pady=10)

        dataset_creator_button = tk.Button(self, text="Dataset Creator", command=self.dataset_creator)
        dataset_creator_button.pack(pady=10)

        quit_button = tk.Button(self, text="Quit", command=self.quit_app)
        quit_button.pack(pady=10)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def data_plot(self):
        self.clear_window()

        # Create a frame for the plot and buttons
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Initialize plot and canvas
        self.obj.create_figure()
        self.fig, self.axs = self.obj.fig, self.obj.axs

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Return Button
        self.return_button = tk.Button(self.frame, text="Return", command=self.stop_updating)
        self.return_button.grid(row=1, column=0, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # State for controlling the update loop
        self.updating = True
        self.update_interval = 1  # Interval in milliseconds (1000 ms = 1 sec)

        # Start updating the plot
        self.update_plot()

    def stop_updating(self):
        self.updating = False
        self.create_main_menu()

    def update_plot(self):
        if self.updating:
            # self.obj.capture_data()
            # self.obj.update_figure()

            self.canvas.draw()
            self.after(self.update_interval, self.update_plot)

    def calibrate(self):
        self.clear_window()

        label = tk.Label(self, text='Calibrating, Keep the Device Still...')
        label.pack(pady=100)

        def calibrate_and_return():
            self.obj.calibrate(self.tc)
            self.create_main_menu()

        thread = threading.Thread(target=calibrate_and_return)
        thread.start()

    def classify(self):
        self.clear_window()

        text_screen = tk.Text(self, height=10, width=40)
        text_screen.pack(pady=10)

        return_button = tk.Button(self, text="Return", command=self.create_main_menu)
        return_button.pack(pady=10)

    def dataset_creator(self):
        self.clear_window()

        # Create a frame for the plot and buttons
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Initialize plot and canvas
        self.obj.create_figure()
        self.fig, self.axs = self.obj.fig, self.obj.axs

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Return Button
        self.return_button = tk.Button(self.frame, text="Cancel", command=self.stop_updating)
        self.return_button.grid(row=1, column=0, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # State for controlling the update loop
        self.updating = True
        self.update_interval = 1
        class_list = ['a','b','c', 'd', 'e']
        self.update_thread = threading.Thread(target=lambda: self.obj.dataset_generator(
                'alphabet2',
                len(class_list) * 3,
                class_list,
                method='automatic'
            ))
        self.update_thread.start()
        self.update_plot()


    def quit_app(self):
        self.destroy()

if __name__ == "__main__":
    tc = 3
    device_name = 'MPU9250'
    box = MPU9250(device_name, hardware_flag=False, ntimesteps=2048)
    app = Application(obj=box, tc=tc)
    app.mainloop()
