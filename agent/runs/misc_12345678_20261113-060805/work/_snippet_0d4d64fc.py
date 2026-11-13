import wave
import struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ouvrir le fichier wav
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Stéréo, 2 bytes par échantillon
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

# Séparer les canaux
left = np.array([samples[i] for i in range(0, len(samples), 2)])
right = np.array([samples[i] for i in range(1, len(samples), 2)])

# Générer spectrogramme du canal gauche
plt.figure(figsize=(15, 5))
plt.specgram(left, Fs=44100, NFFT=1024, noverlap=512)
plt.title('Spectrogramme - Canal Gauche')
plt.xlabel('Temps (s)')
plt.ylabel('Fréquence (Hz)')
plt.savefig('spectrogram_left.png', dpi=150)
print("Spectrogramme gauche sauvegardé")

# Générer spectrogramme du canal droit
plt.figure(figsize=(15, 5))
plt.specgram(right, Fs=44100, NFFT=1024, noverlap=512)
plt.title('Spectrogramme - Canal Droit')
plt.xlabel('Temps (s)')
plt.ylabel('Fréquence (Hz)')
plt.savefig('spectrogram_right.png', dpi=150)
print("Spectrogramme droit sauvegardé")

# Générer spectrogramme de la différence
diff = left - right
plt.figure(figsize=(15, 5))
plt.specgram(diff, Fs=44100, NFFT=1024, noverlap=512)
plt.title('Spectrogramme - Différence')
plt.xlabel('Temps (s)')
plt.ylabel('Fréquence (Hz)')
plt.savefig('spectrogram_diff.png', dpi=150)
print("Spectrogramme différence sauvegardé")

print("\nFichiers générés:")
import os
for f in os.listdir('.'):
    if f.endswith('.png'):
        print(f"  {f}")