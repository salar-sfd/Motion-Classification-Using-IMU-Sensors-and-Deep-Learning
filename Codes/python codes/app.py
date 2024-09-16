import tkinter as tk
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
        self.title('IMU')
        self.geometry('1000x500')
        self.buttons = []
        self.textboxes = []
        self.entries = []
        self.button_font = ['Verdana', 12]
        self.button_bg = '#072F57' 
        self.button_dbg = '#041A30' 
        self.button_fg = 'white' 
        self.bg = 'gray' 
        self.configure(bg=self.bg)  
        self.create_main_menu()

    def resize_buttons(self, event):
        button_width = event.width*2 // 3  
        button_height = min(self.winfo_height() // 8, 3*event.height // (4*len(self.buttons)))
        self.button_font[1] = min(button_width//20, button_height//4) 

        padding_y = (button_height//6)
        for i, button in enumerate(self.buttons):
            button.config(font=self.button_font)
            button.place(width=button_width, height=button_height, x=event.width//2 - button_width//2, y=padding_y + i*(button_height + padding_y * 2))
    
    def resize_texboxes(self, event):
        textbox_width = event.width*2 // 3
        textbox_height = event.height*5 // 6
        padding_y = self.winfo_height() // 48
        for i, widget in enumerate(self.textboxes):
            if i==0:
                widget.place(width=textbox_width, height=textbox_height//5, x=event.width//2 - textbox_width//2, y=padding_y)
                widget.config(font=self.button_font)
            else:
                widget.place(width=textbox_width, height=textbox_height-padding_y, x=event.width//2 - textbox_width//2, y=padding_y+textbox_height//5)
                widget.config(font=self.button_font)

    def resize_entries(self, event):
        entry_width = event.width*2 // 4
        entry_height = event.height 
        button_width = event.width*2 // 12
        button_height = entry_height
        padding_y = self.winfo_height() // 48

        for entry, button in self.entries:
            entry.config(font=self.button_font)
            entry.place(width=entry_width, height=entry_height-padding_y, x=event.width//2 - (entry_width+button_width)//2, y=padding_y)
            button.config(font=self.button_font, bg=self.button_bg, fg=self.button_fg)
            button.place(width=button_width, height=button_height-padding_y, x=event.width//2 + (entry_width-button_width)//2, y=padding_y)

    def create_main_menu(self):
        self.clear_window()

        button_frame = tk.Frame(self, bg=self.bg)
        button_frame.pack(expand=True, fill=tk.BOTH)
        button_frame.bind('<Configure>', self.resize_buttons)

        classify_button = tk.Button(button_frame, text='Classify', command=self.select_model, font=self.button_font, bg=self.button_bg, fg=self.button_fg)
        classify_button.place()

        calibrate_button = tk.Button(button_frame, text='Calibrate', command=self.calibrate, font=self.button_font, bg=self.button_bg, fg=self.button_fg)
        calibrate_button.place()

        plot_button = tk.Button(button_frame, text='Plot Data', command=self.plot_data, font=self.button_font, bg=self.button_bg, fg=self.button_fg)
        plot_button.place()

        dataset_creator_button = tk.Button(button_frame, text='Modify Datasets', command=self.select_dataset, font=self.button_font, bg=self.button_bg, fg=self.button_fg)
        dataset_creator_button.place()

        motion_text = 'Motion Detection: ' + ('Hardware' if self.obj.hardware_flag else 'Software')
        motion_detection_button = tk.Button(button_frame, text=motion_text, command=self.swap_flag, font=self.button_font, bg='#125E29' if self.obj.hardware_flag else '#5C000E', fg=self.button_fg)
        motion_detection_button.place()

        quit_button = tk.Button(button_frame, text='Quit', command=self.quit_app, font=self.button_font, bg=self.button_dbg, fg=self.button_fg)
        quit_button.place()

        self.buttons = [classify_button, calibrate_button, plot_button, dataset_creator_button, motion_detection_button, quit_button]

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def plot_data(self):
        self.clear_window()

        self.frame = tk.Frame(self, bg=self.bg)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.fig, self.axs = plt.subplots(2, 2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        button_frame = tk.Frame(self.frame, bg=self.bg)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.return_button = tk.Button(button_frame, text='Return', command=self.return_to_main_menu, fg=self.button_fg, bg=self.button_dbg)
        self.return_button.pack(side=tk.LEFT, padx=5)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.updating = True
        self.update_interval = 1
        
        self.capture_and_plot()

    def return_to_main_menu(self):
        self.updating = False
        self.create_main_menu()

    def return_to_select_dataset(self):
        self.updating = False
        self.select_dataset()

    def capture_and_plot(self):
        if self.updating:
            self.obj.capture_data()
            self.update_figure()
            self.canvas.draw()
            self.after(self.update_interval, self.capture_and_plot)

    def calibrate(self):
        self.clear_window()

        frame = tk.Frame(self, bg=self.bg)
        frame.pack(expand=True, fill=tk.BOTH)
        frame.bind('<Configure>', self.resize_texboxes)
        self.textboxes = []
        label = tk.Label(frame, text='Calibrating...', font=self.button_font, fg=self.button_fg, bg='#5C000E')
        label.place()
        self.textboxes.append(label)

        def calibrate_and_return():
            self.obj.calibrate(self.tc)
            self.after(0, self.create_main_menu)
        thread = threading.Thread(target=calibrate_and_return)
        thread.start()

    def select_model(self):
        self.clear_window()

        model_directory = 'Models'
        try:
            model_names = [os.path.splitext(f)[0] for f in os.listdir(model_directory) if os.path.isfile(os.path.join(model_directory, f))]
        except FileNotFoundError:
            print('Model directory not found.')
            model_names = []
        model_names = list(set(model_names))
        
        self.buttons = []
        button_frame = tk.Frame(self, bg=self.bg)
        button_frame.pack(expand=True, fill=tk.BOTH)
        button_frame.bind("<Configure>", self.resize_buttons)

        for model_name in model_names:
            button = tk.Button(button_frame, text=model_name, command=lambda model_name=model_name: self.classify(model_name) , font=self.button_font, bg=self.button_bg, fg=self.button_fg)
            button.place()
            self.buttons.append(button)
        
        return_button = tk.Button(button_frame, text='Return', command=self.create_main_menu, font=self.button_font, bg=self.button_dbg, fg=self.button_fg)
        return_button.place()
        self.buttons.append(return_button)

    def classify(self, model_name):
        self.clear_window()

        grid_frame = tk.Frame(self, bg=self.bg)
        grid_frame.pack(expand=True, fill=tk.BOTH)
        
        textbox_frame = tk.Frame(grid_frame, bg=self.bg)
        button_frame = tk.Frame(grid_frame, bg=self.bg)

        textbox_frame.grid(row=0, column=0, sticky='nsew')
        button_frame.grid(row=1, column=0, sticky='nsew')
        grid_frame.rowconfigure(0, weight=5)
        grid_frame.rowconfigure(1, weight=1)

        grid_frame.columnconfigure(0, weight=1)

        self.classified_text = []

        textbox_frame.bind('<Configure>', self.resize_texboxes)
        self.textboxes = []
        label = tk.Label(textbox_frame, text='Classified Text', font=self.button_font, bg=self.button_bg, fg=self.button_fg, anchor='w')
        label.pack()
        self.textboxes.append(label)
        self.text_screen = tk.Text(textbox_frame, font=self.button_font)
        self.text_screen.place()
        self.textboxes.append(self.text_screen)

        button_frame.bind('<Configure>', self.resize_buttons)
        self.buttons = []
        return_button = tk.Button(button_frame, text='Return', command=self.return_to_main_menu, font=self.button_font, bg=self.button_dbg, fg=self.button_fg)
        return_button.place()
        self.buttons.append(return_button)

        self.model_name = model_name
        self.obj.load_model(model_name)
        self.obj.model.eval()

        self.updating = True
        self.update_interval = 1
        self.capture_and_classify()

    def capture_and_classify(self):
        if self.updating:
            self.obj.capture_data()
            if self.obj.new_action:
                label = self.obj.classify_action()
                label = '\n' if label=='\\n' else '\b' if label=='\\b' else ' ' if label=='\s' else label
                if(len(label)>1):
                     self.text_screen.delete(1.0, tk.END)
                if(label=='\b'):
                    last_char_index = self.text_screen.index('end-2c')
                    self.text_screen.delete(last_char_index, tk.END)
                else:
                    self.text_screen.insert(tk.END, label)
            self.after(self.update_interval, self.capture_and_classify)

    def select_dataset(self):
        self.clear_window()
        
        grid_frame = tk.Frame(self, bg=self.bg)
        grid_frame.pack(expand=True, fill=tk.BOTH)

        textbox_frame = tk.Frame(grid_frame, bg=self.bg)
        entry_frame = tk.Frame(grid_frame, bg=self.bg)
        button_frame = tk.Frame(grid_frame, bg=self.bg)

        textbox_frame.grid(row=0, column=0, sticky='nsew')
        entry_frame.grid(row=1, column=0, sticky='nsew')
        button_frame.grid(row=2, column=0, sticky='nsew')
        grid_frame.rowconfigure(0, weight=2)
        grid_frame.rowconfigure(1, weight=1)
        grid_frame.rowconfigure(2, weight=6)

        grid_frame.columnconfigure(0, weight=1)

        
        textbox_frame.bind('<Configure>', self.resize_texboxes)
        self.textboxes = []
        label = tk.Label(textbox_frame, text='Classes Separated by Space:', font=self.button_font, bg=self.button_bg, fg=self.button_fg, anchor='w')
        label.pack()
        self.textboxes.append(label)
        self.text_screen1 = tk.Text(textbox_frame, font=self.button_font)
        self.text_screen1.place()
        self.textboxes.append(self.text_screen1)

        entry_frame.bind('<Configure>', self.resize_entries)
        self.entries = []
        self.entry = tk.Entry(entry_frame, font=self.button_font)
        self.entry.place()
        new_button = tk.Button(entry_frame, text='Create New', command=lambda: self.helper_func(self.entry.get()))
        new_button.place()
        self.entries.append((self.entry, new_button))

        dataset_directory = 'Datasets'
        try:
            dataset_names = [os.path.splitext(f)[0] for f in os.listdir(dataset_directory) if os.path.isfile(os.path.join(dataset_directory, f))]
        except FileNotFoundError:
            print('Model directory not found.')
            dataset_names = []
        dataset_names = list(set(dataset_names))

        button_frame.bind("<Configure>", self.resize_buttons)
        self.buttons = []
        for dataset_name in dataset_names:
            button = tk.Button(button_frame, text=dataset_name, command=lambda dataset=dataset_name: self.helper_func(dataset), font=self.button_font, bg=self.button_bg, fg=self.button_fg)
            button.place()
            self.buttons.append(button)
        return_button = tk.Button(button_frame, text='Return', command=self.return_to_main_menu, font=self.button_font, bg=self.button_dbg, fg=self.button_fg)
        return_button.place()
        self.buttons.append(return_button)
            
    def helper_func(self, dataset_name):
        class_list = self.text_screen1.get("1.0", tk.END).strip().split()
        self.dataset_name = dataset_name
        self.class_list = class_list
        self.modify_dataset()
        
    def modify_dataset(self):
        self.clear_window()

        self.frame = tk.Frame(self, bg=self.bg)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.fig, self.axs = plt.subplots(2, 2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        button_frame = tk.Frame(self.frame, bg=self.bg)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.cancel_button = tk.Button(button_frame, text='Cancel', command=self.return_to_select_dataset, fg=self.button_fg, bg=self.button_dbg)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text='Delete Last', command=self.delete_last_action, fg=self.button_fg, bg=self.button_bg)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text='Save', command=self.save_dataset, fg=self.button_fg, bg=self.button_bg)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.updating = True
        self.update_interval = 1

        self.x_new = []
        self.y_new = []
        self.n = 0
        self.update_figure(f'                 Next Class:{self.class_list[0]}      n = {0}')
        self.canvas.draw()
        self.capture_and_create()

    def capture_and_create(self):
        if self.updating:
            self.obj.capture_data()
            if self.obj.new_action:
                cls = self.class_list[(self.n)%len(self.class_list)]
                self.x_new.append(self.obj.action_arr)
                self.y_new.append(cls)
                self.update_figure(f'Class: {cls}     Next Class: {self.class_list[(self.n+1)%len(self.class_list)]}      n = {self.n+1}')
                self.canvas.draw()

                self.obj.new_action = 0
                self.n += 1
                # print(self.y_new[-1])
            self.after(self.update_interval, self.capture_and_create)
    
    def delete_last_action(self):
        if(self.n==0):
            return
        
        self.x_new.pop(-1)
        self.y_new.pop(-1)
        self.obj.action_arr = self.obj.action_arr*0 if self.n==1 else self.x_new[-1]
        self.obj.new_action = 0
        self.n -= 1
        
        self.update_figure(f'Class: {self.class_list[(self.n-1)%len(self.class_list)]}     Next Class: {self.class_list[(self.n)%len(self.class_list)]}      n = {self.n}')
        self.canvas.draw()

    def save_dataset(self):
        self.clear_window()
        self.updating = False
        
        folder_path = 'Datasets'
        full_path = folder_path+'/'+self.dataset_name+'.npz'
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
            text = (f'{len(self.y_new)} new samples added to previous {len(y_old)} samples. The total number of samples: {len(y)}')
        else:
            np.savez(full_path, x=self.x_new, y=self.y_new)
            text = (f'{len(self.y_new)} new samples added. The total number of samples: {len(self.y_new)}')

        label = tk.Label(self, text=text)
        label.pack(pady=100)

        def pause():
            time.sleep(2)
            self.after(0, self.select_dataset)
        thread = threading.Thread(target=pause)
        thread.start()

    def swap_flag(self):
        self.clear_window()
        self.obj.hardware_flag = False if self.obj.hardware_flag else True
        self.create_main_menu()

    def update_figure(self, suptitle='IMU Data Plotter'):
        self.fig.suptitle(suptitle)
        for axs in self.axs:
            for ax in axs:
                ax.cla()
        self.axs[0][0].plot(self.obj.data_arr[:, 0:3], label = ['x', 'y', 'z'])
        self.axs[0][0].plot(self.obj.flag_arr, label = 'f')
        self.axs[0][0].set_ylim([-2.5, 2.5])
        self.axs[0][0].set_title('Accelometer')
        self.axs[0][1].plot(self.obj.action_arr[:, 0:3], label = ['x', 'y', 'z'])
        self.axs[0][1].set_ylim([-2.5, 2.5])
        self.axs[0][1].set_title('Accelometer Last Action')
        self.axs[1][0].plot(self.obj.data_arr[:, 3:6], label = ['x', 'y', 'z'])
        self.axs[1][0].plot(self.obj.flag_arr, label = 'f')
        self.axs[1][0].set_ylim([-1.5, 1.5])
        self.axs[1][0].set_title('Gyroscope')
        self.axs[1][1].plot(self.obj.action_arr[:, 3:6], label = ['x', 'y', 'z'])
        self.axs[1][1].set_ylim([-1.5, 1.5])
        self.axs[1][1].set_title('Gyroscope Last Action')

        for axs in self.axs:
            for ax in axs:
                ax.grid(True)
                ax.legend(loc='upper right')

        if(self.obj.flag_arr[-1]):
            self.fig.set_facecolor('red')
        else:
            self.fig.set_facecolor(self.bg)
    
    def quit_app(self):
        self.obj.close()
        self.destroy()

if __name__ == '__main__':
    tc = 3
    device_name = 'MPU9250'
    box = MPU9250(device_name, hardware_flag=False, ntimesteps=2048)
    app = Application(obj=box, tc=tc)
    app.mainloop()
    os._exit(0)
