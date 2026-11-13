import wave

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Extraire le LSB de chaque byte
lsb_bits = [b & 1 for b in data]

# Convertir en bytes (8 bits par byte)
lsb_bytes = []
for i in range(0, len(lsb_bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (lsb_bits[i + j] << (7 - j))
    lsb_bytes.append(byte_val)

# Afficher en ASCII si imprimable
result = ''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes[:200])
print("LSB (tous les bytes):")
print(result)
print()

# Afficher les valeurs brutes des premiers bytes LSB
print("Premiers 50 bytes LSB:", lsb_bytes[:50])