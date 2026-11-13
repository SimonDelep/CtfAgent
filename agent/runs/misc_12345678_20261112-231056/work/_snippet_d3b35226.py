import wave
import struct

# Ouvrir le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    frames = wav.readframes(wav.getnframes())

# Extraire tous les échantillons
samples = []
for i in range(0, len(frames), 2):
    sample = struct.unpack('<h', frames[i:i+2])[0]
    samples.append(sample)

# Extraire le LSB de chaque échantillon
lsb_bits = [s & 1 for s in samples]

# Regrouper par bytes avec ordre MSB first (bit 7 est le premier)
lsb_bytes_msb = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << (7 - j))  # MSB first
    lsb_bytes_msb.append(byte_val)

print("Avec MSB first:")
print(f"Premiers 50 bytes: {lsb_bytes_msb[:50]}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes_msb[:50])}")

# Chercher le motif "csaw{"
target = b'csaw{'
for i in range(len(lsb_bytes_msb) - 4):
    if lsb_bytes_msb[i:i+5] == list(target):
        print(f"\nTrouvé 'csaw{' à l'index {i}")
        print(f"Contexte: {''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes_msb[max(0,i-10):i+30])}")
        break