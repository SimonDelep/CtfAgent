import struct
from collections import Counter

with open('audio.wav', 'rb') as f:
    data = f.read()

idx = data.find(b'data')
data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+data_size]

num_samples = len(audio_data) // 4

# Extraire le canal droit
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

# Regardons les séquences qui ne sont PAS de longueur 1
non_one_seqs = [seq for seq in right_zero_seqs if seq != 1]
print(f"Nombre de séquences != 1: {len(non_one_seqs)}")
print(f"Premières 50 séquences != 1: {non_one_seqs[:50]}")

# Peut-être que seules les séquences >= 2 sont significatives
# Et que les séquences de longueur 1 sont des espaces entre éléments d'une même lettre

# Autre idée: peut-être que le canal gauche contient aussi des informations
# et qu'il faut les combiner

# Extraire le canal gauche
left_samples = []
for i in range(num_samples):
    offset = i * 4
    left = struct.unpack('<h', audio_data[offset:offset+2])[0]
    left_samples.append(left)

left_zero_seqs = find_zero_sequences_ordered(left_samples)
print(f"\nSéquences de zéros canal gauche (non-1): {[seq for seq in left_zero_seqs if seq != 1][:50]}")