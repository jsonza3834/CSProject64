# view.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class View:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        
        self.create_widgets()
        self.count = 0
        self.target_frequency_index = 0
        self.rt60 = 0

    def create_widgets(self):
        # Labels
        self.gfile_label = ttk.Label(self.root, text="File Name :")
        self.gfile_label.grid(column=1, row=3, columnspan=2)

        self.channels_label = ttk.Label(self.root, text=f"number of channels = ")
        self.channels_label.grid(column=1, row=6, columnspan=2)

        self.samplerate_label = ttk.Label(self.root, text=f"sample rate = 0Hz")
        self.samplerate_label.grid(column=1, row=7, columnspan=2)

        self.length_label = ttk.Label(self.root, text=f"length = 0s")
        self.length_label.grid(column=1, row=8, columnspan=2)

        self.message_label = ttk.Label(self.root, text="")
        self.message_label.grid(column=1, row=12, columnspan=2)

        self.high_label = ttk.Label(self.root, text="High RT60 is ____Hz at __.__s")
        self.high_label.grid(column=1, row=9, columnspan=2)

        self.mid_label = ttk.Label(self.root, text="Middle RT60 is ____Hz at __.__s")
        self.mid_label.grid(column=1, row=10, columnspan=2)

        self.low_label = ttk.Label(self.root, text="Low RT60 is ____Hz at __.__s")
        self.low_label.grid(column=1, row=11, columnspan=2)

        # Tkinter Open button
        self.open_button = ttk.Button(
            self.root,
            text='Open a File',
            command=self.select_file
        )
        self.open_button.grid(column=1, row=1)

        # Tkinter Analyze button
        self.analyze_button = ttk.Button(
            self.root,
            text='Analyze File',
            command=self.analyze_file
        )
        self.analyze_button.grid(column=2, row=1)

        self.analyze_button.grid_forget()

        # Tkinter Swap Graphs button
        self.swap_graphs_button = ttk.Button(
            self.root,
            text='Swap graphs',
            command=self.swap_graphs
        )
        self.swap_graphs_button.grid(column=1, row=5, columnspan=2)
        
        # Waveform Graph
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title('Waveform Graph')
        self.ax.set_xlabel('Sample')
        self.ax.set_ylabel('Amplitude')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=1, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')


    def select_file(self):
        filetypes = (
            ('Sound files', '*.wav *.m4a *.aac *.mp3'),
            ('All files', '*.*')
        )

        filename = tk.filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.gfile = filename

        # Update the view
        self.gfile_label.config(text=f"File Name: {filename}")

        # Call the analyze_file method from the model
        self.analyze_file()

        # Tkinter Analyze button
        self.analyze_button = ttk.Button(
            self.root,
            text='Analyze File',
            command=self.analyze_file
        )
        self.analyze_button.grid(column=2, row=1)

    def swap_graphs(self):
        if self.count == 5:
            self.plot_waveform()
            self.count = 0
        elif self.count == 0:
            plt.clf()
            self.plot_spectogram()
            self.count += 1
        elif self.count == 1:
            plt.clf()
            self.plot_high_rt60()
            self.count += 1
        elif self.count == 2:
            plt.clf()
            self.plot_middle_rt60()
            self.count += 1
        elif self.count == 3:
            plt.clf()
            self.plot_low_rt60()
            self.count += 1
        elif self.count == 4:
            plt.clf()
            self.plot_combined()
            self.count += 1
        

    def analyze_file(self):
        # Call the analyze_file method from the model
        self.controller.process_audio(self.controller.output_path)
        
        self.model.analyze_file(self.controller.output_path)

        # Call the plot_waveform method from the view
        self.plot_waveform()
        
        self.count = 0
        self.analyze_button.grid_forget()

    def plot_waveform(self):
        # Waveform Graph
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title('Waveform Graph')
        self.ax.set_xlabel('Sample')
        self.ax.set_ylabel('Amplitude')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=1, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')
        # gathering data for the waveform plot
        self.channels_label.config(text=f"number of channels = {self.model.channels}")
        self.samplerate_label.config(text=f"sample rate = {self.model.samplerate}Hz")
        length = round(self.model.data.shape[0] / self.model.samplerate, 2)
        self.length_label.config(text=f"length = {length}s")
        
        self.ax.plot(self.model.data)
        self.canvas.draw()

    def plot_spectogram(self):
        # Intensity Graph
        spectrum, freqs, t, im = plt.specgram(self.model.data, Fs=self.model.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        cbar.set_label('Intensity (dB)')
        # drawing the intensity/spectogram graph
        plt.xlabel('Time (s)')
        plt.ylabel('frequency (Hz)')
        plt.title('Frequency Graph')
        self.canvas.draw()

    # calculates and plots the high frequency RT60 Graph
    def plot_high_rt60(self):
        # RT60 High Graph
        self.plot_rt60("High", 1000, 5000, '#004bc6')
        self.high_label.config(text=f"High RT60 is {int(self.model.freqs[self.target_frequency_index])}Hz at {round(abs(self.rt60), 2)}s")
        self.canvas.draw()

    def plot_low_rt60(self):
        # RT60 Low Graph
        self.plot_rt60("Low", 20, 200, '#c67a00')
        self.low_label.config(text=f"Low RT60 is {int(self.model.freqs[self.target_frequency_index])}Hz at {round(abs(self.rt60), 2)}s")
        self.canvas.draw()

    def plot_middle_rt60(self):
        # RT60 Mid Graph
        self.plot_rt60("Middle", 200, 1000, '#c600b6')
        self.mid_label.config(text=f"Middle RT60 is {int(self.model.freqs[self.target_frequency_index])}Hz at {round(abs(self.rt60), 2)}s")
        self.canvas.draw()

    def plot_rt60(self, freq_range, low_freq, high_freq, color):
        # Find indices of frequencies within the specified range
        indices = np.where((self.model.freqs >= low_freq) & (self.model.freqs <= high_freq))[0]
        # Find the frequency with maximum intensity within the specified range
        self.target_frequency_index = indices[np.argmax(np.max(self.model.spectrum[indices, :], axis=1))]

        data_in_db = self.model.frequency_check(self.model.freqs[self.target_frequency_index])

        # plots a dot at the highest frequency
        plt.plot(self.model.t[self.target_frequency_index], data_in_db[self.target_frequency_index], 'go')

        # plotting a yellow dot at the -5db mark
        value_of_max_less_5 = data_in_db[self.target_frequency_index] - 5
        value_of_max_less_5 = self.model.find_nearest_value(data_in_db, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(self.model.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

        # plotting a red dot at the -25db mark
        value_of_max_less_25 = data_in_db[self.target_frequency_index] - 25
        value_of_max_less_25 = self.model.find_nearest_value(data_in_db, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(self.model.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

        # calculating the RT20 value
        rt20 = (self.model.t[index_of_max_less_5] - self.model.t[index_of_max_less_25])[0]

        # calculating the RT60 value
        self.rt60 = 3 * rt20

        plt.plot(self.model.t, data_in_db, alpha=0.7, color=color)
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        plt.title(f'{freq_range} RT60 Graph')


    def plot_combined(self):
        # RT60 Combined Graph
        plt.clf()
        self.plot_rt60("Combined", 1000, 5000, '#004bc6')
        self.plot_rt60("Combined", 20, 200, '#c67a00')
        self.plot_rt60("Combined", 200, 1000, '#c600b6')
        self.canvas.draw()
