import wave

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Les bytes impairs semblent avoir un motif
# Regardons les valeurs des bytes impairs
odd_bytes = [data[i] for i in range(1, len(data), 2)]

print("Premiers 100 bytes impairs:", odd_bytes[:100])

# Combien de 255, 0, 1, etc.
from collections import Counter
counter = Counter(odd_bytes[:1000])
print("\nDistribution des valeurs (premiers 1000 bytes impairs):")
for val, count in sorted(counter.items())[:20]:
    print(f"  {val}: {count}")

# Peut-être que le LSB des bytes impairs contient le message
lsb_odd = [b & 1 for b in odd_bytes]
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (bits[i + j] << (7 - j))
        result.append(byte_val)
    return result

odd_lsb_bytes = bits_to_bytes(lsb_odd)
print("\nLSB des bytes impairs (premières 50 valeurs):", odd_lsb_bytes[:50])
print("En ASCII:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in odd_lsb_bytes[:100]))