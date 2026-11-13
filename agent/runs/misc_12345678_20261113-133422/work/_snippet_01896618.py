import wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    params = wav.getparams()
    n_channels = params.nchannels
    sampwidth = params.sampwidth
    framerate = params.framerate
    n_frames = params.nframes
    
    # Lire les données
    data = wav.readframes(n_frames)
    
print(f"Channels: {n_channels}, Sample width: {sampwidth}, Framerate: {framerate}, Frames: {n_frames}")

# Convertir en numpy array
if sampwidth == 2:
    dtype = np.int16
elif sampwidth == 1:
    dtype = np.int8
else:
    dtype = np.int16

data_array = np.frombuffer(data, dtype=dtype)

# Séparer les canaux si stéréo
if n_channels == 2:
    left = data_array[0::2]
    right = data_array[1::2]
else:
    left = data_array
    right = data_array

print(f"Left samples: {len(left)}, Right samples: {len(right)}")

# Générer spectrogramme
plt.figure(figsize=(15, 8))
plt.specgram(left, Fs=framerate, NFFT=1024, noverlap=512, cmap='hot')
plt.title('Spectrogram - Left Channel')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar()
plt.savefig('spectrogram_left.png', dpi=150)
plt.close()

# Spectrogramme du canal droit
plt.figure(figsize=(15, 8))
plt.specgram(right, Fs=framerate, NFFT=1024, noverlap=512, cmap='hot')
plt.title('Spectrogram - Right Channel')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar()
plt.savefig('spectrogram_right.png', dpi=150)
plt.close()

print("Spectrogrammes générés: spectrogram_left.png, spectrogram_right.png")