import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from view import View
from model import Model
import numpy as np

class Controller:
    def __init__(self, root, model, view, output_file_path):
        self.root = root
        self.model = model
        self.view = view
        self.output_path = output_file_path
        self.setup_callbacks()

    def process_audio(self, output_path):
        
        audio_data = self.model.read_audio(self.view.gfile)
        self.model.convert_to_wav(audio_data, output_path)
        
        wav_data = self.model.read_wav(output_path)
        self.model.mono_channel(wav_data)
        self.model.remove_metadata(wav_data, output_path)

    def setup_callbacks(self):
        self.view.open_button.config(command=self.select_file)
        self.view.analyze_button.config(command=self.analyze_file)

    def select_file(self):
        filetypes = (
            ('Sound files', '*.wav *.m4a *.aac *.mp3'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.view.gfile = filename

        # Update the view
        self.view.gfile_label.config(text=f"File Name: {filename}")

        
        # Tkinter Analyze button
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
        self.view.count = 0
        self.view.analyze_button.grid_forget()     

        
