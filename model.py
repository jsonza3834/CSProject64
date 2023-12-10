# model.py
import wave
from scipy.io import wavfile
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
class Model:
    def __init__(self):
        self.samplerate = 0
        self.data = None
        self.channels = 0
        self.freqs = None
        self.spectrum = None
        self.t = None
        self.im = None

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
