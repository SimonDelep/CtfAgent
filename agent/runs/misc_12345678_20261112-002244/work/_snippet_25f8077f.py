import wave
import struct

# Lire le fichier WAV
w = wave.open('audio.wav', 'rb')
frames = w.readframes(w.getnframes())
w.close()

# Convertir en samples (stéréo, 16-bit)
samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)

print(f"Nombre de samples: {len(samples)}")
print(f"Premiers 20 samples: {samples[:20]}")
print(f"Derniers 20 samples: {samples[-20:]}")

# Vérifier si c'est du silence ou du bruit
min_val = min(samples)
max_val = max(samples)
print(f"Min: {min_val}, Max: {max_val}")

# Vérifier la distribution
non_zero = sum(1 for s in samples if s != 0)
print(f"Samples non nuls: {non_zero} sur {len(samples)}")