import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import scipy.io
from scipy.io import wavfile


gfile = ''
# create the root window
root = tk.Tk()
root.title('Interactive Data Acoustic Modeling')
root.resizable(False, False)
root.geometry('625x800')


''' 
tkinter.filedialog.askopenfilenames(**options) 
Create an Open dialog and  
return the selected filename(s) that correspond to  
existing file(s). 
'''


def select_file():
    global gfile
    filetypes = (
        ('Sound files', '*.wav'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    gfile = filename

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename
    )

    gfile_label.config(text=f"File Name: {filename}")

def analyze_file():
    ax.clear()
    wav_fname = gfile
    samplerate, data = wavfile.read(wav_fname)

    channels_label.config(text=f"number of channels = {data.shape[len(data.shape) - 1]}")

    samplerate_label.config(text=f"sample rate = {samplerate}Hz")

    length = data.shape[0] / samplerate

    length_label.config(text=f"length = {length}s")

    ax.plot(data)
    canvas.draw()


# Labels
gfile_label = ttk.Label(root, text="File Name :")
gfile_label.grid(column=1, row=2, columnspan=2)

channels_label = ttk.Label(root, text=f"number of channels = ")
channels_label.grid(column=1, row=4, columnspan=2)

samplerate_label = ttk.Label(root, text=f"sample rate = 0Hz")
samplerate_label.grid(column=1, row=5, columnspan=2)

length_label = ttk.Label(root, text=f"length = 0s")
length_label.grid(column=1, row=6, columnspan=2)

# Tkinter Open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.grid(column=1, row=1, padx=8, pady=8, sticky='w')

# Tkinter Analyze button
analyze_button = ttk.Button(
    root,
    text='Analyze File',
    command=analyze_file
)

analyze_button.grid(column=2, row=1, padx=10, pady=10, sticky='e')

# Plotting the Data
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('Waveform Graph')
ax.set_xlabel('Sample')
ax.set_ylabel('Amplitude')

# Tkinter Graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=3, columnspan=2, padx=10, pady=10, sticky='nsew')


# run the application
root.mainloop()

