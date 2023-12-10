import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import scipy.io
from scipy.io import wavfile
import wave
import audio_metadata
from pydub import AudioSegment
import numpy as np
import tempfile

gfile = ''
global show
show = True

# create the root window
root = tk.Tk()
root.title('Interactive Data Acoustic Modeling')
root.resizable(False, False)
root.geometry('1250x800')

file_path_var = tk.StringVar()


def select_file():
    global gfile
    filetypes = (
        ('Sound files', '*.wav *.m4a *.aac *.mp3'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    gfile = filename
    file_path_var.set(gfile)

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename
    )

    gfile_label.config(text=f"File Name: {filename}")


def analyze_file(file_path):
    global show
    ax.clear()
    iax.clear()
    ax.set_title('Waveform Graph')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')
    iax.set_title('Frequency Graph')
    iax.set_xlabel('Frequency (Hz)')
    iax.set_ylabel('Time (s)')
    wav_fname = file_path
    with wave.open(wav_fname, 'rb') as wav_read:
        channels = wav_read.getnchannels()
    samplerate, data = wavfile.read(wav_fname)
    spectrum, freqs, t, im = plt.specgram(data, Fs=samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    if show:
        cbar = plt.colorbar(im)
        cbar.set_label('Intensity (dB)')
        show = False

    intensityG.draw()

    channels_label.config(text=f"number of channels = {channels}")

    samplerate_label.config(text=f"sample rate = {samplerate}Hz")

    length = round(data.shape[0] / samplerate, 2)

    length_label.config(text=f"length = {length}s")

    ax.plot(data)
    canvas.draw()


def clean_file():
    global gfile
    gfile = remove_metadata(gfile)
    gfile = handle_multi_channel(gfile)
    root.after(100, lambda: analyze_file(gfile))


# Labels
gfile_label = ttk.Label(root, text="File Name :")
gfile_label.grid(column=1, row=3, columnspan=2)

channels_label = ttk.Label(root, text=f"number of channels = ")
channels_label.grid(column=1, row=5, columnspan=2)

samplerate_label = ttk.Label(root, text=f"sample rate = 0Hz")
samplerate_label.grid(column=1, row=6, columnspan=2)

length_label = ttk.Label(root, text=f"length = 0s")
length_label.grid(column=1, row=7, columnspan=2)

message_label = ttk.Label(root, text="")
message_label.grid(column=1, row=8, columnspan=2)

# Tkinter Open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.grid(column=1, row=1)

# Tkinter Analyze button
analyze_button = ttk.Button(
    root,
    text='Analyze File',
    command=lambda: analyze_file(gfile)
)

analyze_button.grid(column=2, row=1)

fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('Waveform Graph')
ax.set_xlabel('Sample')
ax.set_ylabel('Amplitude')

ifig, iax = plt.subplots(figsize=(6, 4))
iax.set_title('Frequency Graph')
iax.set_xlabel('Frequency (Hz)')
iax.set_ylabel('Time (s)')

# Waveform Graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')

# Intensity Graph
intensityG = FigureCanvasTkAgg(ifig, master=root)
intensityG_widget = intensityG.get_tk_widget()
intensityG_widget.grid(column=3, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')


def convert_to_wav(file_path):
    # Convert to wav format
    audio = AudioSegment.from_file(file_path)
    
    if format != "wav":
        audio.export(output_path, format="wav")

    return file_path
    
def remove_metadata(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        metadata = audio_metadata.load(file_path)
        if metadata.tags:
            display_message("Metadata tags found. Removing...")
            metadata.clear()  # Remove all tags
            audio.export(file_path, format="wav", tags={})  # Export to the same file with empty tags
            display_message("Metadata tags removed.")
    except audio_metadata.UnsupportedFormat:
        display_message("Not a supported audio format")

    return file_path


def handle_multi_channel(file_path):
    audio = AudioSegment.from_file(file_path)
    channels = audio.channels

    if channels > 1:
        display_message("Multi-channel audio detected. Converting to one channel...")
        convert_to_mono(file_path)
        display_message("Conversion to one channel complete")

    return file_path


def display_message(message):
    message_label.config(text=message)


def convert_to_mono(input_file):
    # Read the input file as raw binary data
    with open(input_file, 'rb') as infile:
        data = infile.read()

    # Create a new WAV file for writing with one channel
    with wave.open(input_file, 'wb') as outfile:
        # Use mono settings
        outfile.setnchannels(1)
        outfile.setsampwidth(2)
        outfile.setframerate(44100)  # Adjust if necessary

        # Write audio data
        outfile.writeframes(data)


root.mainloop()
