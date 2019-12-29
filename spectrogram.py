import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

mic = pyaudio.PyAudio()

INTERVAL = 0.32

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = int(RATE * INTERVAL)

stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(data, dtype='b')
    f, t, Sxx = signal.spectrogram(data, fs=CHUNK)
    dBS = 10 * np.log10(Sxx)
    plt.clf()
    plt.pcolormesh(t, f, dBS)
    plt.pause(0.001)
    
stream.stop_stream()
stream.close()
mic.terminate()
