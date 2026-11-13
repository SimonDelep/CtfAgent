import struct
import wave
from collections import Counter

with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())

samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)

# Regardons toutes les valeurs (positives et négatives)
# Peut-être que les valeurs entre -8 et 8 sont importantes

# Extraire les valeurs entre -8 et 8 (exclus 0)
relevant_samples = [s for s in samples if -8 <= s <= 8 and s != 0]
print(f"Nombre de valeurs entre -8 et 8 (exclus 0): {len(relevant_samples)}")

# Distribution des valeurs
counts = Counter(relevant_samples)
print("\nDistribution des valeurs:")
for v in sorted(counts.keys()):
    print(f"  {v}: {counts[v]}")

# Peut-être que les valeurs positives et négatives représentent des bits
# ou qu'elles sont utilisées différemment

# Essayons de voir si les valeurs positives et négatives alternent d'une manière particulière
# ou si elles forment un pattern

# Regardons les transitions entre valeurs positives et négatives
transitions = []
for i in range(len(relevant_samples) - 1):
    if relevant_samples[i] > 0 and relevant_samples[i+1] < 0:
        transitions.append('pos->neg')
    elif relevant_samples[i] < 0 and relevant_samples[i+1] > 0:
        transitions.append('neg->pos')
    elif relevant_samples[i] > 0 and relevant_samples[i+1] > 0:
        transitions.append('pos->pos')
    else:
        transitions.append('neg->neg')

trans_counts = Counter(transitions)
print(f"\nTransitions:")
for k, v in trans_counts.items():
    print(f"  {k}: {v}")

# Peut-être que c'est un code où les valeurs positives représentent 1 et les négatives 0
# ou vice versa

# Essayons de convertir en binaire: positif = 1, négatif = 0
bits = [1 if s > 0 else 0 for s in relevant_samples]
print(f"\nPremiers 100 bits: {bits[:100]}")

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
text = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_list[:200])
print(f"Texte: {text}")

# Peut-être que c'est du texte encodé en ASCII
# Regardons si on trouve des patterns
print(f"\nOctets en hex: {bytes(bytes_list[:50]).hex()}")