import struct
import wave
from collections import Counter

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Extraire les valeurs positives entre 1 et 8
positive_sequence = [s for s in samples if 1 <= s <= 8]

# Peut-être que c'est un code où chaque valeur représente un caractère
# et qu'il faut trouver le mapping correct

# Regardons la séquence complète et essayons de trouver des patterns
# Peut-être que le message est juste la séquence de valeurs elle-même

# Essayons de voir si la séquence contient "csaw" en cherchant des patterns
# Peut-être que c'est un code où on doit lire les valeurs différemment

# Autre idée: peut-être que c'est du base8 mais en utilisant les valeurs comme chiffres
# et qu'on doit convertir en texte en lisant par groupes de N valeurs

# Essayons de trouver la longueur du message en supposant que c'est du texte ASCII
# Si chaque caractère est représenté par N valeurs, alors len(positive_sequence) / N = longueur du message

# Pour un flag csaw{...}, on s'attend à environ 20-50 caractères
# Donc N serait environ 895041 / 30 = ~30000, ce qui est trop grand

# Peut-être que le message est plus long, ou peut-être que c'est un code différent

# Regardons les valeurs négatives - peut-être qu'elles indiquent des séparateurs
# ou qu'elles sont importantes pour le décodage

# Essayons de voir si les valeurs négatives ont un pattern
negative_samples = [s for s in samples if s < 0]
print(f"Nombre de valeurs négatives: {len(negative_samples)}")

# Peut-être que les valeurs négatives sont du bruit et que seules les valeurs positives comptent
# Ou peut-être que les valeurs négatives indiquent des séparateurs entre les caractères

# Regardons la distribution des valeurs négatives
from collections import Counter
neg_counts = Counter(negative_samples)
print(f"\nValeurs négatives les plus fréquentes:")
for val, count in neg_counts.most_common(10):
    print(f"  {val}: {count}")

# Peut-être que les valeurs négatives sont toutes proches de -32768 (le minimum pour 16-bit signed)
# et qu'elles représentent du silence ou du bruit

# Regardons les valeurs autour de -32768
near_min = [s for s in negative_samples if s >= -32768 and s <= -32000]
print(f"\nValeurs entre -32768 et -32000: {len(near_min)}")

# Peut-être que les valeurs négatives sont du bruit et que seules les valeurs positives comptent
# Et que le message est encodé dans les valeurs positives

# Essayons de voir si la séquence de valeurs positives contient un message
# en utilisant un mapping simple

# Peut-être que c'est un code où chaque valeur représente un caractère
# et qu'il faut trouver le mapping correct

# Regardons si on peut trouver "csaw" en cherchant des patterns dans la séquence
# Peut-être que c'est un code où on doit lire les valeurs différemment

# Autre idée: peut-être que c'est du base8 mais en utilisant les valeurs comme chiffres
# et qu'on doit convertir en texte en lisant par groupes de N valeurs

# Essayons de convertir la séquence en une chaîne de chiffres et de la lire comme du texte encodé
digit_str = ''.join(str(v) for v in positive_sequence)

# Peut-être que c'est du base10 encodé? Ou du ASCII en décimal?
# Essayons de lire par groupes de 2 ou 3 chiffres

# Essayons de convertir par groupes de 2 chiffres (base 10)
def try_decimal_groups(digit_str, group_size):
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

# Essayons avec différents group sizes
for gs in [2, 3, 4]:
    text = try_decimal_groups(digit_str[:gs*50], gs)
    print(f"Groupes de {gs} (décimal): {text}")

# Peut-être que c'est du base8 (octal) mais en utilisant les valeurs 1-8 comme chiffres
# Et on doit convertir en texte en lisant par groupes de 2 ou 3

# Essayons de convertir par groupes de 2 chiffres octaux (en utilisant 1-8 comme chiffres)
def try_octal_groups(seq, group_size):
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

for gs in [2, 3]:
    text = try_octal_groups(positive_sequence[:gs*50], gs)
    print(f"Octal groupes de {gs}: {text}")