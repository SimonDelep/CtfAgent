import struct
import wave
from collections import Counter

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Décoder avec A=1
decoded = ''.join(chr(ord('A') + v - 1) for v in positive_sequence)

# La lettre la plus fréquente dans notre décodage est A (232162 fois)
# En anglais, E est la lettre la plus fréquente
# Donc peut-être que A -> E, ce qui signifie un décalage de +4

# Essayons de décaler de +4 (A->E, B->F, etc.)
shift = 4
shifted = ''.join(chr(ord('A') + ((ord(c) - ord('A') + shift) % 26)) for c in decoded[:200])
print(f"Shift +4: {shifted}")

# Essayons tous les décalages
for shift in range(26):
    shifted = ''.join(chr(ord('A') + ((ord(c) - ord('A') + shift) % 26)) for c in decoded[:100])
    # Vérifier si on trouve des mots anglais courants
    if 'the' in shifted.lower() or 'and' in shifted.lower() or 'flag' in shifted.lower() or 'csaw' in shifted.lower():
        print(f"Shift {shift}: {shifted}")

# Peut-être que c'est plus simple: peut-être que les valeurs 1-8 représentent
# directement des lettres, mais dans un ordre différent

# Regardons si on peut trouver "csaw" en cherchant des patterns dans la séquence
# Peut-être que c'est un code où chaque valeur correspond à une lettre spécifique

# Autre idée: peut-être que c'est du base8 mais en utilisant les valeurs comme chiffres
# et qu'on doit convertir en texte en lisant par groupes

# Essayons de convertir la séquence en une chaîne de chiffres et de la lire comme du texte encodé
digit_str = ''.join(str(v) for v in positive_sequence)

# Peut-être que c'est du base10 encodé? Ou du ASCII en décimal?
# Essayons de lire par groupes de 2 ou 3 chiffres

def try_decimal_encoding(digit_str, group_size):
    result = []
    for i in range(0, len(digit_str) - group_size + 1, group_size):
        try:
            val = int(digit_str[i:i+group_size])
            if 32 <= val < 127:
                result.append(chr(val))
            else:
                result.append('?')
        except:
            result.append('?')
    return ''.join(result)

print(f"\nGroupes de 2 (décimal): {try_decimal_encoding(digit_str[:200], 2)}")
print(f"Groupes de 3 (décimal): {try_decimal_encoding(digit_str[:300], 3)}")

# Peut-être que c'est du base8 (octal) mais en utilisant les valeurs 1-8 comme chiffres
# Et on doit convertir en texte en lisant par groupes de 2 ou 3

# Essayons de convertir par groupes de 2 chiffres octaux (en utilisant 1-8 comme chiffres)
def try_octal_encoding(seq, group_size):
    result = []
    for i in range(0, len(seq) - group_size + 1, group_size):
        try:
            # Convertir les valeurs en chiffres (1-8 -> 1-8)
            octal_str = ''.join(str(v) for v in seq[i:i+group_size])
            val = int(octal_str, 8)
            if 32 <= val < 127:
                result.append(chr(val))
            else:
                result.append('?')
        except:
            result.append('?')
    return ''.join(result)

print(f"\nOctal groupes de 2: {try_octal_encoding(positive_sequence[:100], 2)}")
print(f"Octal groupes de 3: {try_octal_encoding(positive_sequence[:150], 3)}")