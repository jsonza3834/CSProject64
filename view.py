# view.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import os


class View:
    # Sets up tkinter, widgets, and variables
    def __init__(self, model):
        self.root = tk.Tk()
        self.root.title('Interactive Data Acoustic Modeling')
        self.root.resizable(False, False)
        self.root.geometry('700x800')
        
        self.model = model
        
        self.create_widgets()
       
        self.target_frequency_index = 0
        self.rt60 = 0

    def create_widgets(self):
        
        # Labels
        self.gfile_label = ttk.Label(self.root, text="File Name:")
        self.gfile_label.grid(column=1, row=3, columnspan=2)

        

        self.length_label = ttk.Label(self.root, text=f"File Length = 0s")
        self.length_label.grid(column=1, row=6, columnspan=2)

        

        self.res_label = ttk.Label(self.root, text="Resonant Frequency: ____ Hz")
        self.res_label.grid(column=1, row=7, columnspan=2)

        self.RT60dif_label = ttk.Label(self.root, text="Difference: __.__s")
        self.RT60dif_label.grid(column=1, row=8, columnspan=2)

        self.message_label = ttk.Label(self.root, text="")
        self.message_label.grid(column=1, row=12, columnspan=2)

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

        
        
        # Tkinter Cycle Freq Graphs button
        self.swap_graphs_button = ttk.Button(
            self.root,
            text='Cycle RT60 Graphs',
            command=self.swap_RT60_graphs
        )
        self.swap_graphs_button.grid(column=2, row=5, columnspan=2)

        self.swap_graphs_button.grid_forget()

        # Tkinter Combine Freq Graphs button
        self.combine_button = ttk.Button(
            self.root,
            text='Combine RT60 Graphs',
            command=self.plot_combined
        )
        self.combine_button.grid(column=2, row=7, columnspan=2)

        self.combine_button.grid_forget()

        # Tkinter Waveform button
        self.waveform_graph_button = ttk.Button(
            self.root,
            text='Waveform Graph',
            command=self.plot_waveform
        )
        self.waveform_graph_button.grid(column=1, row=5, columnspan=2)

        self.waveform_graph_button.grid_forget()

        # Tkinter Intensity button
        self.intensity_graph_button = ttk.Button(
            self.root,
            text='Intensity Graph',
            command= self.plot_spectogram
        )
        self.intensity_graph_button.grid(column=0, row=5, columnspan=2)

        self.intensity_graph_button.grid_forget()
        
        # Canvas set up graph
        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.ax.set_title('Default Graph')
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=1, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')


    # Swaps between RT60 graphs
    def swap_RT60_graphs(self):
        if self.count == 0:
            plt.clf()
            self.plot_low_rt60()
            self.count += 1
        elif self.count == 1:
            plt.clf()
            self.plot_middle_rt60()
            self.count += 1
        elif self.count == 2:
            plt.clf()
            self.plot_high_rt60()
            self.count = 0

    # Plots a waveform graph
    def plot_waveform(self):
        # Waveform Graph
        
        time_values = np.arange(0, len(self.model.data)) / self.model.samplerate
        
        plt.clf()
        plt.plot(time_values, self.model.data)
        plt.title('Waveform Graph')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
      
        self.canvas.draw()
        
        
        length = round(self.model.data.shape[0] / self.model.samplerate, 2)
        self.length_label.config(text=f"File Length = {length}s")

    # Plots a spectogram graph
    def plot_spectogram(self):
        plt.clf()
        # Intensity Graph
        spectrum, freqs, t, im = plt.specgram(self.model.data, Fs=self.model.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        cbar.set_label('Intensity (dB)')
        # drawing the intensity/spectogram graph
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Frequency Graph')
        self.canvas.draw()

    # Calculates and plots the frequenciesRT60 Graph
    def plot_high_rt60(self):
        # RT60 High Graph
        self.plot_rt60("High", 1000, 5000, '#004bc6')
        
        self.canvas.draw()

    def plot_low_rt60(self):
        # RT60 Low Graph
        self.plot_rt60("Low", 20, 250, '#c67a00')
        
        self.canvas.draw()

    def plot_middle_rt60(self):
        # RT60 Mid Graph
        self.plot_rt60("Middle", 250, 1000, '#c600b6')
        
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

        #Plot RT60
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
        
        justname = os.path.basename(filename)

        # Update the view
        self.gfile_label.config(text=f"File Name: {justname}")

        # Call the analyze_file method from the model
        self.analyze_file()

        # Tkinter Analyze button
        self.analyze_button = ttk.Button(
            self.root,
            text='Analyze File',
            command=self.analyze_file
        )
        self.analyze_button.grid(column=2, row=1)

    # Analyzes the file using methods from modle and controller
    def analyze_file(self):
        # Process the audio
        self.controller.process_audio(self.controller.output_path)
        # Call the analyze_file method from the model
        self.model.analyze_file(self.controller.output_path)

    # root.mainloop for Tkinter
    def mainloop(self):
            self.root.mainloop()
