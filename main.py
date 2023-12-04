import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from pydub import AudioSegment
import os
import scipy.io.wavfile as wavfile

gfile = ''
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

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

def convert_to_wav(input_file):
    if not input_file.lower().endswith(".wav"):
        output_file = os.path.splitext(input_file)[0] + ".wav"
        audio = AudioSegment.from_mp3(input_file)
        audio.export(output_file, format="wav")
        print("file was not wav, converting now...")
        return output_file
    return input_file

def analyze_file():
    global gfile
    wav_fname = convert_to_wav(gfile)
    samplerate, data = wavfile.read(wav_fname)
    print(f"Number of channels = {data.shape[len(data.shape) - 1]}")
    print(f"Sample rate = {samplerate}Hz")
    length = data.shape[0] / samplerate
    print(f"Length = {length}s")

open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

root.mainloop()

