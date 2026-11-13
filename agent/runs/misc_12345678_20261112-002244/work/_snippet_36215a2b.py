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

# Essayer différentes clés XOR
keys_to_try = [
    b'csaw',
    b'flag',
    b'test',
    b'12345678',
    b'01234567',
    bytes(range(8)),  # 0,1,2,3,4,5,6,7
    bytes([i % 256 for i in range(8)]),
]

for key in keys_to_try:
    xored = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    if b'csaw{' in xored:
        idx = xored.index(b'csaw{')
        print(f"Found 'csaw{{' with key {key!r} at index {idx}")
        print(xored[idx:idx+100])
        break
else:
    # Chercher juste "csaw" sans "{"
    for key in keys_to_try:
        xored = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        if b'csaw' in xored:
            idx = xored.index(b'csaw')
            print(f"Found 'csaw' with key {key!r} at index {idx}")
            print(xored[idx:idx+50])
            break
    else:
        print("No 'csaw' found with common keys")
        
        # Peut-être que le message est juste le LSB sans XOR
        # Chercher "{" dans data brut
        if b'{' in data:
            idx = data.index(b'{')
            print(f"Found '{{' in raw data at index {idx}")
            print(data[max(0,idx-20):idx+40])