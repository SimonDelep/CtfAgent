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

# Hypothèse: chaque séquence de zéros représente un élément Morse
# Longueur 1-3 = point (.)
# Longueur 4-6 = trait (-)
# Longueur >= 7 = séparateur entre lettres

# Essayons ce mapping
def decode_morse(seqs):
    result = []
    current_letter = []
    
    for seq in seqs:
        if seq >= 7:  # séparateur entre lettres
            if current_letter:
                result.append(''.join(current_letter))
                current_letter = []
            result.append(' ')  # séparateur de mot (ou espace)
        elif seq <= 3:  # point
            current_letter.append('.')
        else:  # trait (4-6)
            current_letter.append('-')
    
    if current_letter:
        result.append(''.join(current_letter))
    
    return ''.join(result)

decoded = decode_morse(right_zero_seqs)
print("Décodage (seuil >= 7 pour séparateur):")
print(decoded[:500])
print("...")
print(decoded[-200:])