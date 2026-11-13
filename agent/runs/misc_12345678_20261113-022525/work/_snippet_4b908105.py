import struct
import wave

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Peut-être que chaque valeur représente un bit (ou plusieurs bits)
# Si 1-8 représente 3 bits (0-7), alors on peut convertir en binaire

# Mais 8 = 1000 en binaire, donc 4 bits...
# Essayons de convertir chaque valeur en binaire et de concaténer

# Autre idée: peut-être que c'est du base8 (octal) mais en utilisant 1-8 comme chiffres
# Et on doit convertir en texte

# Essayons: chaque valeur - 1 donne 0-7, qui est valide en octal
octal_digits = [v - 1 for v in positive_sequence]
octal_str = ''.join(str(d) for d in octal_digits[:100])
print(f"Octal string (premier 100): {octal_str}")

# Maintenant essayons de convertir par groupes de 2 ou 3
# Si c'est de l'ASCII en octal, chaque caractère est 2 ou 3 chiffres octaux

# Essayons de lire par groupes de 2 chiffres octaux
def octal_to_text(octal_str, group_size=2):
    result = []
    for i in range(0, len(octal_str) - group_size + 1, group_size):
        try:
            val = int(octal_str[i:i+group_size], 8)
            if 32 <= val < 127:
                result.append(chr(val))
            else:
                result.append('?')
        except:
            result.append('?')
    return ''.join(result)

print(f"Groupes de 2: {octal_to_text(octal_str, 2)[:50]}")
print(f"Groupes de 3: {octal_to_text(octal_str, 3)[:50]}")

# Peut-être que c'est du base64? Ou un autre encodage
# Essayons de voir si la séquence contient des patterns de base64

# Autre idée: peut-être que les valeurs 1-8 représentent des lettres A-H
# Et le message est en ROT ou autre substitution

# Regardons la séquence complète et essayons de la décoder comme si c'était du texte
# en utilisant un mapping A=1, B=2, etc.

decoded = ''.join(chr(ord('A') + v - 1) for v in positive_sequence)
print(f"\nDécodé (A=1): {decoded[:200]}")

# Peut-être que c'est du ROT13 ou autre
import codecs
rot13 = codecs.decode(decoded[:200], 'rot_13')
print(f"ROT13: {rot13}")

# Ou peut-être que c'est un code où on doit lire les valeurs différemment
# Essayons de voir si c'est du base8 mais en utilisant les valeurs directement
# et en convertissant en texte

# Autre approche: peut-être que c'est un code où chaque groupe de N valeurs
# représente un caractère

# Essayons de trouver la longueur du message en supposant que c'est du texte ASCII
# Si chaque caractère est représenté par N valeurs, alors len(positive_sequence) / N = longueur du message

# Pour un flag csaw{...}, on s'attend à environ 20-50 caractères
# Donc N serait environ 895041 / 30 = ~30000, ce qui est trop grand

# Peut-être que le message est plus long, ou peut-être que c'est un code différent

# Regardons les valeurs négatives - peut-être qu'elles indiquent des séparateurs
negative_indices = [i for i, s in enumerate(samples) if s < 0]
print(f"\nNombre de valeurs négatives: {len(negative_indices)}")

# Peut-être que les valeurs négatives séparent les valeurs positives en groupes
# Et chaque groupe représente un caractère

# Regardons la distribution des longueurs de groupes de valeurs positives
groups = []
current_group = []
for s in samples:
    if 1 <= s <= 8:
        current_group.append(s)
    else:
        if current_group:
            groups.append(current_group)
            current_group = []
if current_group:
    groups.append(current_group)

print(f"Nombre de groupes: {len(groups)}")
print(f"Longueurs des premiers 20 groupes: {[len(g) for g in groups[:20]]}")

# Distribution des longueurs de groupes
from collections import Counter
group_lens = Counter(len(g) for g in groups)
print(f"\nDistribution des longueurs de groupes:")
for k in sorted(group_lens.keys())[:20]:
    print(f"  {k}: {group_lens[k]}")