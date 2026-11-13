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

print(f"Channels: {n_channels}, Sample width: {sampwidth}, Framerate: {framerate}, Frames: {n_frames}")

# Convertir en samples
if sampwidth == 2:
    fmt = '<h' if n_channels == 1 else '<hh'
    samples = struct.unpack(fmt * (n_frames // n_channels), frames)
    
    if n_channels == 2:
        left = samples[0::2]
        right = samples[1::2]
        
        # Différence entre canaux
        diff = [abs(l - r) for l, r in zip(left, right)]
        
        # Trouver les pics dans la différence
        max_diff = max(diff)
        print(f"Max diff: {max_diff}")
        
        # Extraire les échantillons où la différence est significative
        significant = [(i, diff[i]) for i in range(len(diff)) if diff[i] > 10000]
        print(f"Significant diffs count: {len(significant)}")
        
        # Afficher les 20 premiers
        for i, d in significant[:20]:
            print(f"Pos {i}: diff={d}, left={left[i]}, right={right[i]}")