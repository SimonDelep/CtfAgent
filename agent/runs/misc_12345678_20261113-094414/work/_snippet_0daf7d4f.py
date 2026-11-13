import wave
import numpy as np

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    print(f"Channels: {wf.getnchannels()}")
    print(f"Sample width: {wf.getsampwidth()}")
    print(f"Frame rate: {wf.getframerate()}")
    print(f"Num frames: {wf.getnframes()}")
    
    # Lire les données
    data = wf.readframes(wf.getnframes())
    
# Convertir en numpy array
if wf.getsampwidth() == 2:  # 16-bit
    data = np.frombuffer(data, dtype=np.int16)
elif wf.getsampwidth() == 1:  # 8-bit
    data = np.frombuffer(data, dtype=np.int8)
else:
    data = np.frombuffer(data, dtype=np.int32)

print(f"Data length: {len(data)}")

# Si stéréo, séparer les canaux
if wf.getnchannels() == 2:
    data = data.reshape(-1, 2)
    left = data[:, 0]
    right = data[:, 1]
    print(f"Left range: {left.min()} to {left.max()}")
    print(f"Right range: {right.min()} to {right.max()}")
    
    # Afficher quelques échantillons du canal droit
    print(f"First 20 right samples: {right[:20]}")
    print(f"Non-zero right samples count: {np.count_nonzero(right)}")
else:
    left = data
    right = None