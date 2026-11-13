import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    
# Convertir en échantillons
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Trouver toutes les séquences de zéros (min_len=6)
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

all_zeros = find_zero_sequences(samples, min_len=6)
lengths = [l for _, l in all_zeros]

print(f"Nombre de séquences: {len(lengths)}")

# Essayer différentes mappings pour convertir en bits
# Hypothèse 1: longueurs paires = 0, impaires = 1
bits_even_odd = [0 if l % 2 == 0 else 1 for l in lengths]
print(f"\nMapping pair/impair: {bits_even_odd[:32]}")

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return result

bytes_even_odd = bits_to_bytes(bits_even_odd)
print(f"Bytes (pair/impair): {bytes_even_odd}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '?' for b in bytes_even_odd)}")

# Hypothèse 2: longueurs <= 7 = 0, > 7 = 1
bits_threshold = [0 if l <= 7 else 1 for l in lengths]
print(f"\nMapping seuil 7: {bits_threshold[:32]}")
bytes_threshold = bits_to_bytes(bits_threshold)
print(f"Bytes (seuil 7): {bytes_threshold}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '?' for b in bytes_threshold)}")

# Hypothèse 3: longueurs <= 8 = 0, > 8 = 1
bits_threshold2 = [0 if l <= 8 else 1 for l in lengths]
print(f"\nMapping seuil 8: {bits_threshold2[:32]}")
bytes_threshold2 = bits_to_bytes(bits_threshold2)
print(f"Bytes (seuil 8): {bytes_threshold2}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '?' for b in bytes_threshold2)}")