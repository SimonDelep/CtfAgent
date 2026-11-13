import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)

# Essayer de voir si le message est dans les bits LSB mais avec un ordre différent
# Peut-être que les bits sont stockés bit par bit dans les samples successifs

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
print("All LSB combined (first 500 bytes):")
print(data[:500])

# Chercher "csaw" ou "{"
if b'csaw' in data:
    idx = data.index(b'csaw')
    print(f"\nFound 'csaw' at index {idx}")
    print(data[idx:idx+50])
    
if b'{' in data:
    idx = data.index(b'{')
    print(f"\nFound '{{' at index {idx}")
    print(data[max(0,idx-10):idx+40])