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

# Filtrer les séquences != 1
filtered_seqs = [seq for seq in right_zero_seqs if seq != 1]

# Distribution des longueurs filtrées
counter = Counter(filtered_seqs)
print("Distribution des séquences != 1:")
for length in sorted(counter.keys()):
    print(f"  {length}: {counter[length]}")

# Peut-être que:
# - Séquences de longueur 2 = point
# - Séquences de longueur 3+ = trait
# - Séquences de longueur >= 8 = séparateur entre lettres

def decode_morse_v3(seqs):
    result = []
    current_letter = []
    
    for seq in seqs:
        if seq >= 8:  # séparateur entre lettres
            if current_letter:
                result.append(''.join(current_letter))
                current_letter = []
            result.append(' ')
        elif seq == 2:  # point
            current_letter.append('.')
        else:  # trait (3-7)
            current_letter.append('-')
    
    if current_letter:
        result.append(''.join(current_letter))
    
    return ''.join(result)

decoded = decode_morse_v3(filtered_seqs)
print("\nDécodage (2=point, 3+=trait, >=8=séparateur):")
print(decoded[:500])
print("...")
print(decoded[-200:])