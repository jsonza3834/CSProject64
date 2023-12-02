import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import scipy.io
from scipy.io import wavfile


gfile = ''
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

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

    gfile_label = ttk.Label(root, text=gfile)
    gfile_label.pack(side="bottom")

    analyze_button = ttk.Button(
        root,
        text='Analyze File',
        command=analyze_file
    )
    analyze_button.pack(expand=True)

def analyze_file():
    wav_fname = gfile
    samplerate, data = wavfile.read(wav_fname)
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    print(f"sample rate = {samplerate}Hz")
    length = data.shape[0] / samplerate
    print(f"length = {length}s")


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

# run the application
root.mainloop()

