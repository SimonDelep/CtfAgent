import struct
import wave

# Recharger le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Essayer: chaque valeur + un offset pour obtenir ASCII
# Peut-être que 1-8 correspond à des lettres spécifiques
# Ou peut-être que c'est un code où chaque nombre représente un caractère

# Regardons la distribution des valeurs
from collections import Counter
counts = Counter(positive_sequence)
print("Distribution des valeurs:")
for v in sorted(counts.keys()):
    print(f"  {v}: {counts[v]} fois ({counts[v]/len(positive_sequence)*100:.2f}%)")

# Essayer un mapping simple: 1->a, 2->b, etc. mais en minuscules
decoded_lower = ''.join(chr(ord('a') + v - 1) for v in positive_sequence[:200])
print(f"\nMapping 1=a: {decoded_lower}")

# Peut-être que c'est du Morse? 1-8 pourrait représenter des points et traits
# Ou peut-être que les valeurs négatives sont importantes aussi

# Regardons les valeurs négatives
negative_samples = [s for s in samples if s < 0]
print(f"\nNombre de valeurs négatives: {len(negative_samples)}")
print(f"Valeurs négatives uniques: {sorted(set(negative_samples))[:20]}")

# Peut-être que le signal est dans la différence entre valeurs positives et négatives
# Ou peut-être que c'est un code où on doit ignorer certaines valeurs

# Essayons de voir si la séquence contient "csaw" ou "flag"
target = "csaw"
target_nums = [ord(c) - ord('a') + 1 for c in target]
print(f"\nRecherche de 'csaw' en nombres: {target_nums}")

# Chercher la séquence dans positive_sequence
for i in range(len(positive_sequence) - len(target_nums)):
    if positive_sequence[i:i+len(target_nums)] == target_nums:
        print(f"Trouvé 'csaw' à la position {i}")
        break
else:
    print("'csaw' non trouvé directement")

# Peut-être que c'est 0-indexé: a=0, b=1, etc.
target_nums_0 = [ord(c) - ord('a') for c in target]
print(f"Recherche de 'csaw' (0-indexé): {target_nums_0}")
for i in range(len(positive_sequence) - len(target_nums_0)):
    if positive_sequence[i:i+len(target_nums_0)] == target_nums_0:
        print(f"Trouvé 'csaw' (0-indexé) à la position {i}")
        break