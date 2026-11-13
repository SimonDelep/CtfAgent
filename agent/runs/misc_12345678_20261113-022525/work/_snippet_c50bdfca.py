import struct
import wave

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Peut-être que c'est un code où chaque nombre correspond à une lettre,
# mais avec un décalage différent. Essayons de trouver un pattern.

# Regardons si la séquence contient des patterns répétitifs
# Ou peut-être que c'est du base8 (octal) mais en utilisant les valeurs comme chiffres

# Essayons de convertir la séquence entière en une chaîne de chiffres et voir si c'est du texte encodé
digit_str = ''.join(str(v) for v in positive_sequence)
print(f"Longueur de la chaîne de chiffres: {len(digit_str)}")

# Peut-être que c'est du base64 encodé en chiffres? Ou du ASCII en octal?
# Essayons de lire par groupes de 2 ou 3 chiffres comme des octets

# Si c'est de l'ASCII en octal, chaque caractère serait représenté par 2 ou 3 chiffres octaux
# Mais 8 n'est pas valide en octal...

# Peut-être que c'est du base9 ou base10?
# Ou peut-être que chaque nombre (1-8) correspond à un bit ou un groupe de bits

# Essayons: chaque nombre représente 3 bits (puisque 1-8 = 001-1000 en binaire)
# Mais 8 = 1000, donc 4 bits...

# Autre idée: peut-être que c'est un code où 1-8 représente des lettres A-H
# Et le message est en anglais codé ainsi

# Regardons la séquence complète et essayons de trouver des mots anglais
# en essayant différents mappings

# D'abord, voyons si on peut trouver "flag" ou "csaw" dans la séquence
# en essayant tous les décalages possibles

def try_mapping(seq, offset):
    return ''.join(chr(ord('a') + ((v - 1 + offset) % 26)) for v in seq[:100])

for offset in range(26):
    decoded = try_mapping(positive_sequence, offset)
    if 'flag' in decoded.lower() or 'csaw' in decoded.lower():
        print(f"Offset {offset}: {decoded}")

# Peut-être que c'est un code où les nombres ne sont pas directement des lettres
# mais représentent des positions dans l'alphabet

# Autre approche: peut-être que c'est du Morse codé avec 1-8
# 1-4 = point, 5-8 = trait? Ou quelque chose comme ça

# Regardons les transitions entre valeurs
transitions = []
for i in range(len(positive_sequence) - 1):
    diff = positive_sequence[i+1] - positive_sequence[i]
    transitions.append(diff)

# Distribution des transitions
from collections import Counter
trans_counts = Counter(transitions)
print("\nDistribution des transitions:")
for k in sorted(trans_counts.keys())[:20]:
    print(f"  {k}: {trans_counts[k]}")