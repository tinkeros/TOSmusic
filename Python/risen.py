import pyaudio
import numpy as np

tempo = 0.95 # smaller is faster
fs = 44100   # sampling rate, Hz
reverb = True
reverb_delay = 0.45
reverb_intensity = 0.35

ticksPerSecond = 560

risen_freqs = [587.3, 0, 659.3, 0, 698.5, 0, 698.5, 0, 659.3, 0, 659.3, 0, 698.5, 0, 587.3, 0, 523.3, 0, 587.3, 0, 587.3, 0, 659.3, 0, 523.3, 0, 784.0, 0, 698.5, 0, 587.3, 0, 659.3, 0, 698.5, 0, 698.5, 0, 659.3, 0, 659.3, 0, 698.5, 0, 587.3, 0, 523.3, 0, 587.3, 0, 587.3, 0, 659.3, 0, 523.3, 0, 784.0, 0, 698.5, 0, 587.3, 0, 523.3, 0, 587.3, 0, 659.3, 0, 440.0, 0, 440.0, 0, 659.3, 0, 659.3, 0, 698.5, 0, 659.3, 0, 587.3, 0, 784.0, 0, 493.9, 0, 587.3, 0, 523.3, 0, 698.5, 0, 587.3, 0, 523.3, 0, 587.3, 0, 659.3, 0, 440.0, 0, 440.0, 0, 659.3, 0, 659.3, 0, 698.5, 0, 659.3, 0, 587.3, 0, 784.0, 0, 493.9, 0, 587.3, 0, 523.3, 0, 698.5, 0]

# in ticks (560 ticks per second)
risen_delays = [101, 10, 101, 10, 203, 21, 203, 22, 67, 8, 67, 7, 67, 7, 204, 21, 100, 10, 101, 10, 101, 11, 101, 10, 67, 7, 67, 7, 67, 7, 101, 10, 101, 11, 203, 21, 203, 22, 67, 7, 67, 7, 68, 7, 203, 21, 101, 10, 101, 10, 101, 10, 101, 10, 67, 7, 67, 7, 67, 7, 101, 10, 101, 10, 203, 21, 203, 21, 101, 10, 101, 10, 67, 7, 67, 7, 68, 6, 68, 6, 68, 7, 68, 7, 67, 7, 67, 7, 67, 7, 205, 19, 101, 10, 101, 11, 203, 21, 203, 21, 101, 11, 101, 10, 68, 6, 68, 6, 67, 7, 67, 7, 67, 7, 67, 7, 67, 7, 68, 7, 67, 7, 203, 0 ]

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

i = 0
samples=None

while (i<len(risen_freqs)):
    duration = tempo*risen_delays[i]/float(ticksPerSecond)

    # round duration so we end this set of samples near a multiple of 2*pi
    if risen_freqs[i]>0:
        duration = int(duration * risen_freqs[i])/risen_freqs[i]

    # generate samples
    new_samples=(np.sin(2*np.pi*np.arange(fs*duration)*risen_freqs[i]/fs)).astype(np.float32)

    if samples is None:
        samples = new_samples
    else:
        samples=np.append(samples,new_samples)

    i+=1

# reverb
if reverb:
    reverb_start = int(reverb_delay*fs)
    for s in range(reverb_start,len(samples)):
        samples[s]=samples[s]+reverb_intensity*samples[s-reverb_start]

# get rid of DC component
samples = samples - np.mean(samples)

samples = np.clip(samples,-1.0,1.0)

stream.write(samples.tobytes())
stream.stop_stream()
stream.close()

p.terminate()
