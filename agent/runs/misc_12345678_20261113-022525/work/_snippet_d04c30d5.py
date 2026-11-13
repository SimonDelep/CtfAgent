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

# La distribution des lettres est:
# A: 232162 (25.94%)
# B: 197750 (22.09%)
# C: 154233 (17.23%)
# D: 111569 (12.47%)
# E: 77445 (8.65%)
# F: 53833 (6.01%)
# G: 38681 (4.32%)
# H: 29368 (3.28%)

# En anglais, la distribution typique est:
# E: ~12.7%, T: ~9.1%, A: ~8.2%, O: ~7.5%, I: ~7.0%, N: ~6.7%, S: ~6.3%, H: ~6.1%, R: ~6.0%, D: ~4.3%, L: ~4.0%, C: ~2.8%, U: ~2.8%, M: ~2.4%, W: ~2.4%, F: ~2.2%, G: ~2.0%, Y: ~2.0%, P: ~1.9%, B: ~1.5%, V: ~1.0%, K: ~0.8%, J: ~0.15%, X: ~0.15%, Q: ~0.10%, Z: ~0.07%

# Notre distribution est très différente, ce qui suggère que c'est peut-être un code simple
# où chaque lettre représente un caractère spécifique

# Peut-être que c'est un code où A=0, B=1, etc. (0-indexé)
# Et qu'on doit convertir en texte en lisant par groupes

# Essayons de convertir la séquence en binaire
# Si chaque valeur 1-8 représente 3 bits (0-7), alors on peut former des octets

# Mais 8 = 1000 en binaire, donc 4 bits...
# Essayons de convertir chaque valeur - 1 en 3 bits (0-7)
bits = []
for v in positive_sequence:
    val = v - 1  # 0-7
    bits.extend([(val >> i) & 1 for i in range(2, -1, -1)])  # 3 bits

print(f"Nombre de bits: {len(bits)}")

# Regrouper par 8 bits pour former des octets
bytes_list = []
for i in range(0, len(bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val = (byte_val << 1) | bits[i + j]
    bytes_list.append(byte_val)

print(f"Nombre d'octets: {len(bytes_list)}")
print(f"Premiers 50 octets: {bytes_list[:50]}")

# Convertir en texte
text = ''.join(chr(b) if 32 <= b < 127 else '?' for b in bytes_list[:100])
print(f"Texte: {text}")

# Peut-être que c'est du texte encodé en ASCII
# Regardons si on trouve des patterns
print(f"\nOctets en hex: {bytes_list[:50].hex()}")