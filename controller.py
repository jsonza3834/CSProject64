# controller.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from view import View
from model import Model
import numpy as np

class Controller:
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view
        self.setup_callbacks()

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
        self.model.analyze_file(self.view.gfile)
        self.view.plot_waveform()
        self.view.count = 0
        self.view.analyze_button.grid_forget()


def main():
    root = tk.Tk()
    root.title('Interactive Data Acoustic Modeling')
    root.resizable(False, False)
    root.geometry('650x800')

    model = Model()
    view = View(root, model)
    controller = Controller(root, model, view)

    root.mainloop()

if __name__ == "__main__":
    main()
