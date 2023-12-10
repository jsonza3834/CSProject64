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
        self.show = True
        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.gfile_label = ttk.Label(self.root, text="File Name :")
        self.gfile_label.grid(column=1, row=3, columnspan=2)

        self.channels_label = ttk.Label(self.root, text=f"number of channels = ")
        self.channels_label.grid(column=1, row=5, columnspan=2)

        self.samplerate_label = ttk.Label(self.root, text=f"sample rate = 0Hz")
        self.samplerate_label.grid(column=1, row=6, columnspan=2)

        self.length_label = ttk.Label(self.root, text=f"length = 0s")
        self.length_label.grid(column=1, row=7, columnspan=2)

        self.message_label = ttk.Label(self.root, text="")
        self.message_label.grid(column=1, row=8, columnspan=2)

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

        # Waveform Graph
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title('Waveform Graph')
        self.ax.set_xlabel('Sample')
        self.ax.set_ylabel('Amplitude')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=1, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')

        # spectogram graph titles and labels
        self.ifig, self.iax = plt.subplots(figsize=(6, 4))
        self.iax.set_title('Frequency Graph')
        self.iax.set_ylabel('Frequency (Hz)')
        self.iax.set_xlabel('Time (s)')

        # Waveform Graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=1, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Intensity Graph
        self.intensityG = FigureCanvasTkAgg(self.ifig, master=self.root)
        self.intensityG_widget = self.intensityG.get_tk_widget()
        self.intensityG_widget.grid(column=3, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')

        # RT60 High Graph
        self.rhtg = FigureCanvasTkAgg(self.ifig, master=self.root)
        self.rhtg_widget = self.rhtg.get_tk_widget()
        self.rhtg_widget.grid(column=1, row=8, columnspan=2, padx=10, pady=10, sticky='nsew')

        # RT60 Low Graph
        self.rltg = FigureCanvasTkAgg(self.ifig, master=self.root)
        self.rltg_widget = self.rltg.get_tk_widget()
        self.rltg_widget.grid(column=3, row=8, columnspan=2, padx=10, pady=10, sticky='nsew')

        # RT60 Mid Graph
        self.rmtg = FigureCanvasTkAgg(self.ifig, master=self.root)
        self.rmtg_widget = self.rmtg.get_tk_widget()
        self.rmtg_widget.grid(column=5, row=8, columnspan=2, padx=10, pady=10, sticky='nsew')

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

    def analyze_file(self):
        # Call the analyze_file method from the model
        self.model.analyze_file(self.gfile)

        # Call the plot_waveform method from the view
        self.plot_waveform()
        self.plot_spectogram()
        self.plot_high_rt60()
        self.plot_low_rt60()
        self.plot_middle_rt60()

    def plot_waveform(self):
        # gathering data for the waveform plot
        self.channels_label.config(text=f"number of channels = {self.model.channels}")
        self.samplerate_label.config(text=f"sample rate = {self.model.samplerate}Hz")
        length = round(self.model.data.shape[0] / self.model.samplerate, 2)
        self.length_label.config(text=f"length = {length}s")

        self.ax.plot(self.model.data)
        self.canvas.draw()

    def plot_spectogram(self):
        plt.clf()
        # the spectogram graph and intensity from the samplerate and data
        spectrum, freqs, t, im = plt.specgram(self.model.data, Fs=self.model.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        # issue with intensity bar creation every button press, this stops that
        if self.show:
            cbar = plt.colorbar(im)
            cbar.set_label('Intensity (dB)')
            self.show = False
        # drawing the intensity/spectogram graph
        self.intensityG.draw()

    # calculates and plots the high frequency RT60 Graph
    def plot_high_rt60(self):
        self.plot_rt60("High", 1000, 5000, self.rhtg)

    def plot_low_rt60(self):
        self.plot_rt60("Low", 20, 200, self.rltg)

    def plot_middle_rt60(self):
        self.plot_rt60("Middle", 200, 1000, self.rmtg)

    def plot_rt60(self, freq_range, low_freq, high_freq, graph_widget):
        plt.clf()
        # Find indices of frequencies within the specified range
        indices = np.where((self.model.freqs >= low_freq) & (self.model.freqs <= high_freq))[0]
        # Find the frequency with maximum intensity within the specified range
        target_frequency_index = indices[np.argmax(np.max(self.model.spectrum[indices, :], axis=1))]

        data_in_db = self.model.frequency_check(self.model.freqs[target_frequency_index])

        # plots a dot at the highest frequency
        plt.plot(self.model.t[target_frequency_index], data_in_db[target_frequency_index], 'go')

        # plotting a yellow dot at the -5db mark
        value_of_max_less_5 = data_in_db[target_frequency_index] - 5
        value_of_max_less_5 = self.model.find_nearest_value(data_in_db, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(self.model.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

        # plotting a red dot at the -25db mark
        value_of_max_less_25 = data_in_db[target_frequency_index] - 25
        value_of_max_less_25 = self.model.find_nearest_value(data_in_db, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(self.model.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

        # calculating the RT20 value
        rt20 = (self.model.t[index_of_max_less_5] - self.model.t[index_of_max_less_25])[0]

        # calculating the RT60 value
        rt60 = 3 * rt20

        print(
            f'The {freq_range} RT60 reverb time at freq {int(self.model.freqs[target_frequency_index])}Hz is {round(abs(rt60), 2)} seconds')

        plt.figure(2)
        plt.plot(self.model.t, data_in_db, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        plt.title(f'{freq_range} RT60 Graph')

        # Update the corresponding canvas widget
        graph_widget.draw()
