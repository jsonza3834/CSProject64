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


gfile = ''

# create the root window
root = tk.Tk()
root.title('Interactive Data Acoustic Modeling')
root.resizable(False, False)
root.geometry('625x800')

file_path_var = tk.StringVar()

def clear_display():
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Label):
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
    file_path_var.set(gfile)

    showinfo(
        title='Selected File',
        message=filename
    )

def analyze_file(file_path):
    clear_display()

    wav_fname = file_path
    with wave.open(wav_fname, 'rb') as wav_read:
        channels = wav_read.getnchannels()
    samplerate, data = wavfile.read(wav_fname)

    gfile_label = ttk.Label(root, text=f"number of channels = {channels}")
    gfile_label.grid(column=1, row=4, columnspan=2)

    gfile_label = ttk.Label(root, text=f"sample rate = {samplerate}Hz")
    gfile_label.grid(column=1, row=5, columnspan=2)

    length = data.shape[0] / samplerate

    gfile_label = ttk.Label(root, text=f"length = {length}s")
    gfile_label.grid(column=1, row=6, columnspan=2)

    ax.plot(data)
    canvas.draw()

def clean_file():
    global gfile
    clear_display()
    gfile = remove_metadata(gfile)
    gfile = handle_multi_channel(gfile)
    root.after(100, lambda: analyze_file(gfile))  # Schedule analyze_file after a short delay

gfile_label = ttk.Label(root, textvariable=file_path_var)
gfile_label.grid(column=1, row=2, columnspan=2)

open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.grid(column=1, row=1, padx=8, pady=8, sticky='w')

analyze_button = ttk.Button(
    root,
    text='Analyze File',
    command=lambda: analyze_file(gfile)
)
analyze_button.grid(column=2, row=1, padx=10, pady=10, sticky='e')

clean_button = ttk.Button(
    root,
    text='Clean File',
    command=clean_file
)
clean_button.grid(column=2, row=2, padx=10, pady=10, sticky='e')

fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('Waveform Graph')
ax.set_xlabel('Sample')
ax.set_ylabel('Amplitude')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=3, columnspan=2, padx=10, pady=10, sticky='nsew')

def remove_metadata(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        metadata = audio_metadata.load(file_path)
        print(metadata)
        if metadata.tags:
            display_message("Metadata tags found. Removing...")
            metadata.clear()  # Remove all tags
            audio.export(file_path, format="wav", tags={})  # Export to the same file with empty tags
            display_message("Metadata tags removed.")
    except audio_metadata.UnsupportedFormat:
        display_message("Not a supported audio format")

    return file_path

def handle_multi_channel(file_path):
    with wave.open(file_path, 'rb') as wav_read:
        channels = wav_read.getnchannels()
        print(channels)

    if channels > 1:
        display_message("Multi-channel audio detected. Converting to one channel...")
        convert_to_mono(file_path)
        display_message("Conversion to one channel complete")

    return file_path

def display_message(message):
    gfile_label = ttk.Label(root, text=message)
    gfile_label.grid(column=1, row=8, columnspan=2)

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

