import wave
import struct
import base64

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())
    samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Extraire tous les LSB
all_lsb = [s & 1 for s in samples]

# Convertir en bytes
lsb_bytes = []
for i in range(0, len(all_lsb) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (all_lsb[i + j] << j)
    lsb_bytes.append(byte_val)

# Essayer de décoder comme Base64
lsb_str = bytes(lsb_bytes)
print("LSB bytes length:", len(lsb_bytes))

# Chercher des motifs Base64
try:
    decoded = base64.b64decode(lsb_str[:1000])
    print("Base64 decoded:", decoded[:100])
except:
    print("Not valid Base64")

# Chercher le motif "csaw{" dans les LSB
target = b"csaw{"
target_bits = []
for c in target:
    for j in range(8):
        target_bits.append((c >> j) & 1)

print("\nSearching for 'csaw{' in LSB...")
for i in range(len(all_lsb) - len(target_bits)):
    if all_lsb[i:i+len(target_bits)] == target_bits:
        print(f"Found at bit position {i}, byte position {i//8}")
        break
else:
    print("Not found in direct LSB")

# Chercher en ordre inverse
all_lsb_rev = all_lsb[::-1]
for i in range(len(all_lsb_rev) - len(target_bits)):
    if all_lsb_rev[i:i+len(target_bits)] == target_bits:
        print(f"Found in reversed LSB at bit position {i}")
        break
