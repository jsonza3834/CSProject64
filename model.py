#modle.py
from pydub import AudioSegment
import os
import tempfile
import tkinter as tk
from tkinter import filedialog as fd
import ffmpeg
import wave
from scipy.io import wavfile
from scipy.signal import welch
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


class Model:
    # Initialize variable for calculations
    def __init__(self):       
        self.samplerate = 0
        self.data = None
        self.channels = 0
        self.freqs = None
        self.spectrum = None
        self.t = None
        self.im = None

    # Read the audio file
    def read_audio(self, file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            return audio
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return None

    # Convert the audio file to .wav
    def convert_to_wav(self, audio_data, output_path):
        # Convert to wav format
        if format != "wav":
            audio_data.export(output_path, format="wav")

    # Read the newly created w.av file
    def read_wav(self, wav_path):
        try:
            wav = AudioSegment.from_file(wav_path)
            return wav
        except Exception as e:
            print(f"Error loading wav file: {e}")
            return None

    # Convert the file to one channel
    def mono_channel(self, wav_file, output_path):
        wav_file = wav_file.set_channels(1)
        wav_file.export(output_path, format="wav")       
            
    # Remove metadat from the file using os
    def remove_metadata(self, wav_file, output_path):
        # Use ffmpeg to remove metadata
        os.system(f'ffmpeg -i "{wav_file}" -map_metadata -1 -acodec copy "{output_path}"')

    # Analyze the file and grab data
    def analyze_file(self, file_path):
        wav_fname = file_path
        with wave.open(wav_fname, 'rb') as wav_read:
            self.channels = wav_read.getnchannels()
        self.samplerate, self.data = wavfile.read(wav_fname)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

    # Calculate the resonance
    def calculate_res(self, file_path):
        frequencies, power = welch(self.data, self.samplerate, nperseg=4096)
        dominant = frequencies[np.argmax(power)]
        return dominant
    
    # Calulate RT60 values
    def RT60(self, low_freq, high_freq):
        # Find indices of frequencies within the specified range
        indices = np.where((self.freqs >= low_freq) & (self.freqs <= high_freq))[0]
        
        # Find the frequency with maximum intensity within the specified range
        self.target_frequency_index = indices[np.argmax(np.max(self.spectrum[indices, :], axis=1))]

        
        data_in_db = self.frequency_check(self.freqs[self.target_frequency_index])

        value_of_max_less_5 = data_in_db[self.target_frequency_index] - 5
        value_of_max_less_5 = self.find_nearest_value(data_in_db, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

        value_of_max_less_25 = data_in_db[self.target_frequency_index] - 25
        value_of_max_less_25 = self.find_nearest_value(data_in_db, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

        # RT20 value
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]

        # Calculating the RT60 value
        self.rt60 = 3 * rt20

        return abs(self.rt60)

    # Calculate the RT60 dif
    def RT60_dif(self, low, mid, high):
        RT60avg = (low + mid + high) / 3
        dif = RT60avg - .5
        return abs(round(dif,2))


    # Checking for frequency
    def frequency_check(self, target_frequency):
        
        # Identify a frequency to check
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
        # Find sound data for a particular frequency
        data_for_frequency = self.spectrum[index_of_frequency]
        # Change a digital signal for a value in decibels
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    # Find the nearest values for plotting
    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    



        
