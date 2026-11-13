import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)

# Extraire tous les LSB
all_lsb = [s & 1 for s in samples]

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return bytes(result)

data = bits_to_bytes(all_lsb)

# Essayer XOR avec "12345678"
key = b'12345678'
xored = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

print("XOR with '12345678' (first 500):")
print(xored[:500])

# Chercher "csaw{"
if b'csaw{' in xored:
    idx = xored.index(b'csaw{')
    print(f"\nFound 'csaw{{' at index {idx}")
    print(xored[idx:idx+100])
else:
    # Chercher juste "csaw"
    if b'csaw' in xored:
        idx = xored.index(b'csaw')
        print(f"\nFound 'csaw' at index {idx}")
        print(xored[idx:idx+50])