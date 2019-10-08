import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

mic = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
CHUNK = int(RATE/20)

stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

fig, ax = plt.subplots(figsize=(14,6))

ax.set_ylim(0, 200)
ax.set_xlim(0, CHUNK)

x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))

while True:
    data = stream.read(CHUNK)
    data = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2]
    data = abs(data)
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.005)

stream.stop_stream()
stream.close()
mic.terminate()

