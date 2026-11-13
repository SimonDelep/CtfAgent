import struct

with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'data')
data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+data_size]

# 2 canaux, 16 bits par échantillon
# BlockAlign = 4 bytes = 2 échantillons de 2 bytes chacun
num_samples = len(audio_data) // 4  # nombre de paires d'échantillons

# Extraire les canaux
left_samples = []
right_samples = []

for i in range(num_samples):
    offset = i * 4
    left = struct.unpack('<h', audio_data[offset:offset+2])[0]
    right = struct.unpack('<h', audio_data[offset+2:offset+4])[0]
    left_samples.append(left)
    right_samples.append(right)

print(f"Total samples: {num_samples}")
print(f"Left samples (first 20): {left_samples[:20]}")
print(f"Right samples (first 20): {right_samples[:20]}")

# Trouver les séquences de zéros (silences)
def find_zero_sequences(samples):
    sequences = []
    current_len = 0
    for s in samples:
        if s == 0:
            current_len += 1
        else:
            if current_len > 0:
                sequences.append(current_len)
            current_len = 0
    if current_len > 0:
        sequences.append(current_len)
    return sequences

left_zeros = find_zero_sequences(left_samples)
right_zeros = find_zero_sequences(right_samples)

print(f"\nLeft zero sequences: {len(left_zeros)}")
print(f"Right zero sequences: {len(right_zeros)}")

# Afficher les longueurs uniques et leurs fréquences
from collections import Counter
print(f"\nLeft zero lengths: {Counter(left_zeros)}")
print(f"\nRight zero lengths: {Counter(right_zeros)}")