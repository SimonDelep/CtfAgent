from collections import Counter

# Données du canal droit
right_zeros = [1]*99564 + [2]*17769 + [3]*6422 + [4]*2889 + [5]*1027 + [6]*485 + [7]*233 + [8]*141 + [9]*71 + [10]*36 + [11]*25 + [12]*21 + [13]*6 + [14]*4 + [15]*3 + [16]*2 + [21]*2 + [18]*1 + [17]*1

# Réanalyser le fichier pour avoir les séquences exactes dans l'ordre
import struct

with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'data')
data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+data_size]

num_samples = len(audio_data) // 4

# Extraire uniquement le canal droit
right_samples = []
for i in range(num_samples):
    offset = i * 4
    right = struct.unpack('<h', audio_data[offset+2:offset+4])[0]
    right_samples.append(right)

# Trouver les séquences de zéros dans l'ordre
def find_zero_sequences_ordered(samples):
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

right_zero_seqs = find_zero_sequences_ordered(right_samples)
print(f"Nombre de séquences: {len(right_zero_seqs)}")
print(f"Premières 50 séquences: {right_zero_seqs[:50]}")

# Afficher les longueurs uniques
unique_lengths = sorted(set(right_zero_seqs))
print(f"Longueurs uniques: {unique_lengths}")