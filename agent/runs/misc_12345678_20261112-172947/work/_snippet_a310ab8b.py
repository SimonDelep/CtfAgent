import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    
# Convertir en échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Séparer les canaux
left_channel = samples[0::2]
right_channel = samples[1::2]

# Trouver les séquences de zéros dans le canal droit uniquement
def find_zero_sequences(samples, min_len=6):
    sequences = []
    current_len = 0
    current_start = 0
    for i, s in enumerate(samples):
        if s == 0:
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            if current_len >= min_len:
                sequences.append((current_start, current_len))
            current_len = 0
    if current_len >= min_len:
        sequences.append((current_start, current_len))
    return sequences

right_zeros = find_zero_sequences(right_channel, min_len=6)
print(f"Séquences de zéros canal droit (>= 6): {len(right_zeros)}")

lengths_right = [l for _, l in right_zeros]
print(f"Longueurs (premières 50): {lengths_right[:50]}")

from collections import Counter
counts = Counter(lengths_right)
print(f"\nComptage des longueurs canal droit:")
for length, count in sorted(counts.items()):
    print(f"  {length}: {count}")

# Essayer de convertir en bits avec différents mappings
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return result

# Mapping: longueur paire = 0, impaire = 1
bits = [0 if l % 2 == 0 else 1 for l in lengths_right]
print(f"\nBits (pair/impair) premières 32: {bits[:32]}")
bytes_result = bits_to_bytes(bits)
print(f"Bytes: {bytes_result[:20]}")
print(f"ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_result[:20])}")

# Mapping: longueur <= 7 = 0, > 7 = 1
bits2 = [0 if l <= 7 else 1 for l in lengths_right]
print(f"\nBits (seuil 7) premières 32: {bits2[:32]}")
bytes_result2 = bits_to_bytes(bits2)
print(f"Bytes: {bytes_result2[:20]}")
print(f"ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_result2[:20])}")