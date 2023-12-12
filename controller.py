#controller.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import os
from view import View
from model import Model
import numpy as np

class Controller:
    # Initialize tools
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.root = self.view.root
        
        self.output_path = "cleaned.wav"
        self.setup_callbacks()

    #  Process the audio using model functions
    def process_audio(self, output_path):

        
        audio_data = self.model.read_audio(self.view.gfile)
        self.model.convert_to_wav(audio_data, output_path)

        
        wav_data = self.model.read_wav(output_path)
        self.model.mono_channel(wav_data, output_path)
        self.model.remove_metadata(wav_data, output_path)

    # Setup button calls
    def setup_callbacks(self):
        self.view.open_button.config(command=self.select_file)
        self.view.analyze_button.config(command=self.analyze_file)

    # Select file function
    def select_file(self):
        filetypes = (
            ('Sound files', '*.wav *.m4a *.aac *.mp3'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        # Set view gfile
        self.view.gfile = filename

        # Set justname to only the name of the file and not the whole path
        justname = os.path.basename(filename)

        # Update the view
        self.view.gfile_label.config(text=f"File Name: {justname}")


        
        # Tkinter Analyze button set back up
        self.view.analyze_button = ttk.Button(
            self.root,
            text='Analyze File',
            command=self.analyze_file
        )
        self.view.analyze_button.grid(column=2, row=1)


    def analyze_file(self):
        # Call the analyze_file method from the model
        self.process_audio(self.output_path)
        
        self.model.analyze_file(self.output_path)

        # Call the plot_waveform method from the view
        self.view.plot_waveform()

        # Display resonance
        res = round(self.model.calculate_res(self.output_path),2)
        self.view.res_label.config(text=f"Resonant Frequency: {res} Hz")

        # Low
        low = self.model.RT60(20,250)
        # Mid
        mid = self.model.RT60(250,1000)
        # High
        high = self.model.RT60(1000,5000)

        # Display RT60 difference
        RT60DIF = self.model.RT60_dif(low,mid,high)
        self.view.RT60dif_label.config(text=f"Difference: {RT60DIF}s")

        # Set count
        self.view.count = 0

        # Make analyze button disappear
        self.view.analyze_button.grid_forget()

        # Make graph controls appear
        self.view.swap_graphs_button.grid(column=2, row=5, columnspan=2)
        self.view.combine_button.grid(column=2, row=7, columnspan=2)
        self.view.waveform_graph_button.grid(column=1, row=5, columnspan=2)
        self.view.intensity_graph_button.grid(column=0, row=5, columnspan=2)

        
