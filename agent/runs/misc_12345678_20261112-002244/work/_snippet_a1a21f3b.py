import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), samples)

# Attends, j'ai fait une erreur - samples n'est pas défini
with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)

# Peut-être que "12345678" indique qu'il faut prendre les samples
# aux positions 1, 2, 3, 4, 5, 6, 7, 8 (ou 0-indexed: 0, 1, 2, 3, 4, 5, 6, 7)
# et extraire le LSB de chaque

# Ou peut-être que c'est une séquence de valeurs à chercher dans les samples

# Autre idée : peut-être que le message est dans les bits LSB, mais qu'il faut
# le lire en utilisant un offset spécifique

# Essayons différents offsets
all_lsb = [s & 1 for s in samples]

def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return bytes(result)

# Essayer différents offsets
for offset in range(16):
    data = bits_to_bytes(all_lsb[offset:])
    if b'csaw{' in data:
        idx = data.index(b'csaw{')
        print(f"Found 'csaw{{' with offset {offset} at index {idx}")
        print(data[idx:idx+100])
        break
    if b'{' in data:
        idx = data.index(b'{')
        print(f"Found '{{' with offset {offset} at index {idx}")
        print(data[max(0,idx-20):idx+40])
        break
else:
    print("No '{' found with offsets 0-15")

# Peut-être que le message est dans les canaux séparés
left = samples[0::2]
right = samples[1::2]

left_lsb = [s & 1 for s in left]
right_lsb = [s & 1 for s in right]

for offset in range(16):
    data = bits_to_bytes(left_lsb[offset:])
    if b'csaw{' in data:
        idx = data.index(b'csaw{')
        print(f"Found 'csaw{{' in left with offset {offset} at index {idx}")
        print(data[idx:idx+100])
        break
    if b'{' in data:
        idx = data.index(b'{')
        print(f"Found '{{' in left with offset {offset} at index {idx}")
        print(data[max(0,idx-20):idx+40])
        break
else:
    print("No '{' found in left channel with offsets 0-15")

for offset in range(16):
    data = bits_to_bytes(right_lsb[offset:])
    if b'csaw{' in data:
        idx = data.index(b'csaw{')
        print(f"Found 'csaw{{' in right with offset {offset} at index {idx}")
        print(data[idx:idx+100])
        break
    if b'{' in data:
        idx = data.index(b'{')
        print(f"Found '{{' in right with offset {offset} at index {idx}")
        print(data[max(0,idx-20):idx+40])
        break
else:
    print("No '{' found in right channel with offsets 0-15")