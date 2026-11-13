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

# En Morse standard:
# - Espace entre éléments d'une lettre = 1 unité
# - Espace entre lettres = 3 unités  
# - Espace entre mots = 7 unités

# Si les séquences de zéros représentent les ESPACES:
# - Séquence courte (1-2) = espace intra-lettre (entre point/trait)
# - Séquence moyenne (3-4) = espace entre lettres
# - Séquence longue (>=7) = espace entre mots

# Mais nous avons besoin de savoir QUOI encoder (points et traits)
# Peut-être que les séquences de zéros SONT les éléments Morse eux-mêmes

# Autre approche: considérer que chaque séquence de zéros est un "silence"
# et que la durée du silence encode le symbole

# Essayons: longueur 1 = point, longueur 2+ = trait
# Et séparateur entre lettres = séquence >= 4

def decode_morse_v2(seqs):
    result = []
    current_letter = []
    
    for seq in seqs:
        if seq >= 4:  # séparateur entre lettres
            if current_letter:
                result.append(''.join(current_letter))
                current_letter = []
            result.append(' ')
        elif seq == 1:  # point
            current_letter.append('.')
        else:  # trait (2-3)
            current_letter.append('-')
    
    if current_letter:
        result.append(''.join(current_letter))
    
    return ''.join(result)

decoded = decode_morse_v2(right_zero_seqs)
print("Décodage (seuil >= 4 pour séparateur, 1=point, 2+=trait):")
print(decoded[:500])
print("...")
print(decoded[-200:])