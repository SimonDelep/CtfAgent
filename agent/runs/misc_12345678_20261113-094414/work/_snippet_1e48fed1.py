import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

# Lire le fichier WAV
rate, data = wav.read('audio.wav')

print(f"Sample rate: {rate}")
print(f"Data shape: {data.shape}")
print(f"Data dtype: {data.dtype}")

# Si stéréo, séparer les canaux
if len(data.shape) == 2:
    left = data[:, 0]
    right = data[:, 1]
    print(f"Left channel range: {left.min()} to {left.max()}")
    print(f"Right channel range: {right.min()} to {right.max()}")
else:
    left = data
    right = None

# Générer spectrogramme du canal droit (le plus silencieux, peut-être caché)
if right is not None:
    plt.figure(figsize=(15, 5))
    plt.specgram(right, Fs=rate, NFFT=1024, noverlap=512, cmap='viridis')
    plt.title('Spectrogram - Right Channel')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.savefig('spectrogram_right.png')
    print("Spectrogram saved to spectrogram_right.png")

# Spectrogramme du canal gauche
plt.figure(figsize=(15, 5))
plt.specgram(left, Fs=rate, NFFT=1024, noverlap=512, cmap='viridis')
plt.title('Spectrogram - Left Channel')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar()
plt.savefig('spectrogram_left.png')
print("Spectrogram saved to spectrogram_left.png")

# Spectrogramme de la différence
if right is not None:
    diff = left - right
    plt.figure(figsize=(15, 5))
    plt.specgram(diff, Fs=rate, NFFT=1024, noverlap=512, cmap='viridis')
    plt.title('Spectrogram - Left - Right Difference')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.savefig('spectrogram_diff.png')
    print("Spectrogram saved to spectrogram_diff.png")

print("Done!")