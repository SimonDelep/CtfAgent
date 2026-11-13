import wave
import struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    frames = wf.readframes(n_frames)

if sampwidth == 2 and n_channels == 2:
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    left = np.array(samples[0::2])
    right = np.array(samples[1::2])
    
    # Créer un spectrogramme du canal gauche
    plt.figure(figsize=(15, 5))
    plt.specgram(left, Fs=framerate, NFFT=1024, noverlap=512)
    plt.title('Spectrogramme - Canal Gauche')
    plt.xlabel('Temps (s)')
    plt.ylabel('Fréquence (Hz)')
    plt.savefig('spectrogram_left.png', dpi=150)
    print("Spectrogramme gauche sauvegardé")
    
    # Et du canal droit
    plt.figure(figsize=(15, 5))
    plt.specgram(right, Fs=framerate, NFFT=1024, noverlap=512)
    plt.title('Spectrogramme - Canal Droit')
    plt.xlabel('Temps (s)')
    plt.ylabel('Fréquence (Hz)')
    plt.savefig('spectrogram_right.png', dpi=150)
    print("Spectrogramme droit sauvegardé")
    
    # Et la différence
    diff = left - right
    plt.figure(figsize=(15, 5))
    plt.specgram(diff, Fs=framerate, NFFT=1024, noverlap=512)
    plt.title('Spectrogramme - Différence')
    plt.xlabel('Temps (s)')
    plt.ylabel('Fréquence (Hz)')
    plt.savefig('spectrogram_diff.png', dpi=150)
    print("Spectrogramme différence sauvegardé")