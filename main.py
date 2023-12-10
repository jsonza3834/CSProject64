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

gfile = ''

# Fun global variables because of scopes
global show
global samplerate
global data
global target_frequency
global freqs
show = True

# create the root window
root = tk.Tk()
root.title('Interactive Data Acoustic Modeling')
root.resizable(False, False)
root.geometry('1250x1000')

file_path_var = tk.StringVar()

# selects a frequency under 1000 kHz
def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
        return x


def frequency_check():
    global target_frequency
    global freqs
    global spectrum
    # identify a frequency to check
    target_frequency = find_target_frequency(freqs)
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    # find sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    # change a digital signal for a value in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun


# finds the nearest values of less 5db
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


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

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename
    )

    gfile_label.config(text=f"File Name: {filename}")


# The long function that does everything
def analyze_file(file_path):
    global show
    global freqs
    global samplerate
    global data
    global spectrum
    # resets the graphs so that the program can be used for multiple files in the same session
    ax.clear()
    iax.clear()
    ax.set_title('Waveform Graph')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')
    iax.set_title('Frequency Graph')
    iax.set_ylabel('Frequency (Hz)')
    iax.set_xlabel('Time (s)')
    # wav information and data
    wav_fname = file_path
    with wave.open(wav_fname, 'rb') as wav_read:
        channels = wav_read.getnchannels()
    samplerate, data = wavfile.read(wav_fname)
    # the spectogram graph and intensity from the samplerate and data
    spectrum, freqs, t, im = plt.specgram(data, Fs=samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    # issue with intensity bar creation every button press, this stops that
    if show:
        cbar = plt.colorbar(im)
        cbar.set_label('Intensity (dB)')
        show = False
    # drawing the intensity/spectogram graph
    intensityG.draw()
    # clears the graph data for the next graph, had issue with spectograph not going away, this fixes that
    plt.clf()
    # plotting the RT60 graph
    data_in_db = frequency_check()
    plt.figure(2)
    plt.plot(t, data_in_db, alpha=0.7, color='#004bc6')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (dB)')
    plt.title('RT60 Graph')
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    # plots a dot at the highest frequency
    plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
    # removed usage of sliced_array because it was only given a 0
    sliced_array = data_in_db[index_of_max]
    value_of_max_less_5 = value_of_max - 5
    # plotting a yellow dot at the -5db mark
    value_of_max_less_5 = find_nearest_value(data_in_db, value_of_max_less_5) # sliced_array used prior
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
    plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
    # plotting a red dot at the -25db mark
    value_of_max_less_25 = value_of_max - 25
    value_of_max_less_25 = find_nearest_value(data_in_db, value_of_max_less_25) # sliced_array used prior
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
    plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
    # calculating the RT20 value
    rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
    # calculating the RT60 value
    rt60 = 3 * rt20
    rtg.draw()
    print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

    # gathering data for the waveform plot
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

# intensity graph titles and labels
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('Waveform Graph')
ax.set_xlabel('Sample')
ax.set_ylabel('Amplitude')

# waveform graph titles and labels
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

# RT60 Graph
rtg = FigureCanvasTkAgg(ifig, master=root)
rtg_widget = rtg.get_tk_widget()
rtg_widget.grid(column=1, row=8, columnspan=2, padx=10, pady=10, sticky='nsew')

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

