import wave
import struct
import numpy as np

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    
# Convertir en échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Séparer les canaux (stéréo)
left_channel = samples[0::2]
right_channel = samples[1::2]

# Trouver les séquences de zéros dans chaque canal
def find_zero_sequences(samples, min_len=5):
    sequences = []
    current_len = 0
    current_start = 0
    for i, s in enumerate(samples):
        if s == 0:
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            if current_len >= min_len:
                sequences.append((current_start, current_len))
            current_len = 0
    if current_len >= min_len:
        sequences.append((current_start, current_len))
    return sequences

left_zeros = find_zero_sequences(left_channel)
right_zeros = find_zero_sequences(right_channel)

print(f"Séquences de zéros canal gauche: {len(left_zeros)}")
print(f"Séquences de zéros canal droit: {len(right_zeros)}")

# Afficher les premières séquences de chaque canal
print("\nCanal gauche (premières 10):")
for start, length in left_zeros[:10]:
    print(f"  Position {start}: {length} échantillons")

print("\nCanal droit (premières 10):")
for start, length in right_zeros[:10]:
    print(f"  Position {start}: {length} échantillons")

# Vérifier si les séquences correspondent entre les deux canaux
print("\nComparaison des positions:")
left_starts = set(s for s, _ in left_zeros)
right_starts = set(s for s, _ in right_zeros)
common = left_starts & right_starts
print(f"Positions communes: {len(common)}")