import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import scipy.io
from scipy.io import wavfile
from pydub import AudioSegment
import wave
import audio_metadata

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

def reset_gui():
    # Destroies all widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()

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

    # checks the file for metadata and removes them
    remove_metadata(wav_fname)

    # reads the file for number of channels then converts them to one channel
    handle_multi_channel(wav_fname)

def remove_metadata(wav_fname):
    try:
        metadata = audio_metadata.load(wav_fname)
        if metadata.tags:
            print("Metadata tags found. Removing...")
            # Remove metadata tags
            metadata.remove_tags()
            metadata.save()
            print("Metadata tags removed.")
    except audio_metadata.UnsupportedFormat:
        # Not a supported audio format
        pass

def handle_multi_channel(wav_fname):
    # Read the WAV file to get the number of channels
    with wave.open(wav_fname, 'rb') as wav_read:
        channels = wav_read.getnchannels()

    # If the file has more than one channel, convert to one channel
    if channels > 1:
        print(f"Multi-channel audio detected. Converting to one channel...")
        convert_to_mono(wav_fname)
        print("Conversion to one channel complete.")

def convert_to_mono(input_file):
    # Read the input file as raw binary data
    with open(input_file, 'rb') as infile:
        data = infile.read()

    # Create a new WAV file for writing with one channel
    with wave.open(input_file, 'wb') as outfile:
        # Use mono settings
        outfile.setnchannels(1)
        outfile.setsampwidth(2)

        # Write audio data
        outfile.writeframes(data)

# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

# run the application
root.mainloop()

