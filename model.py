from pydub import AudioSegment
import os
import tempfile
import tkinter as tk
from tkinter import filedialog as fd
import ffmpeg
import wave
from scipy.io import wavfile
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self):
        #self.file_path = 
        #self.wav_path = wav_path
        #self.audio_data = self.read_audio()
        
        self.samplerate = 0
        self.data = None
        self.channels = 0
        self.freqs = None
        self.spectrum = None
        self.t = None
        self.im = None


    
    def read_audio(self, file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            return audio
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return None

    def convert_to_wav(self, audio_data, output_path):
        # Convert to wav format
        if format != "wav":
            audio_data.export(output_path, format="wav")

    def read_wav(self, wav_path):
        try:
            wav = AudioSegment.from_file(wav_path)
            return wav
        except Exception as e:
            print(f"Error loading wav file: {e}")
            return None
        
    def mono_channel(self, wav_file):
        if wav_file:
            # Convert to one channel if multichannel
            if wav_file.channels > 1:
                wav_file = wav_file.set_channels(1)
                
            

    def remove_metadata(self, wav_file, output_path):
        # Use ffmpeg to remove metadata
        os.system(f'ffmpeg -i "{wav_file}" -map_metadata -1 -acodec copy "{output_path}"')


    def analyze_file(self, file_path):
        wav_fname = file_path
        with wave.open(wav_fname, 'rb') as wav_read:
            self.channels = wav_read.getnchannels()
        self.samplerate, self.data = wavfile.read(wav_fname)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))


    
    def find_target_frequency(self, freqs):
            for x in freqs:
                if x > 1000:
                    break
                return x

    def frequency_check(self, target_frequency):
        # identify a frequency to check
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
        # find sound data for a particular frequency
        data_for_frequency = self.spectrum[index_of_frequency]
        # change a digital signal for a value in decibels
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    



        
