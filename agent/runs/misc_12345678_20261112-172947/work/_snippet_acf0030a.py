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

# Extraire les LSB de chaque canal
def extract_lsb(channel):
    bits = []
    for s in channel:
        bits.append(abs(s) & 1)
    return bits

left_bits = extract_lsb(left_channel)
right_bits = extract_lsb(right_channel)

print(f"Nombre de bits LSB canal gauche: {len(left_bits)}")
print(f"Nombre de bits LSB canal droit: {len(right_bits)}")

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return result

left_bytes = bits_to_bytes(left_bits)
right_bytes = bits_to_bytes(right_bits)

print(f"\nCanal gauche - premiers 50 bytes: {left_bytes[:50]}")
print(f"ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in left_bytes[:50])}")

print(f"\nCanal droit - premiers 50 bytes: {right_bytes[:50]}")
print(f"ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in right_bytes[:50])}")

# Chercher "csaw" ou "{" dans les bytes
def find_pattern(bytes_list, pattern):
    pattern_bytes = [ord(c) for c in pattern]
    for i in range(len(bytes_list) - len(pattern_bytes)):
        if bytes_list[i:i+len(pattern_bytes)] == pattern_bytes:
            return i
    return -1

print(f"\nRecherche de 'csaw' dans canal gauche: {find_pattern(left_bytes, 'csaw')}")
print(f"Recherche de 'csaw' dans canal droit: {find_pattern(right_bytes, 'csaw')}")
print(f"Recherche de '{'{' }' dans canal gauche: {find_pattern(left_bytes, '{')}")
print(f"Recherche de '{'{' }' dans canal droit: {find_pattern(right_bytes, '{')}")