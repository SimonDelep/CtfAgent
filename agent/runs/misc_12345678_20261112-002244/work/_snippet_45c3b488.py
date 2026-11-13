import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)
    
# Séparer canaux gauche et droit
left = samples[0::2]
right = samples[1::2]

print(f"Left samples: {len(left)}")
print(f"Right samples: {len(right)}")

# Extraire LSB de chaque canal
def extract_lsb(samples):
    bits = []
    for s in samples:
        bits.append(s & 1)
    return bits

left_bits = extract_lsb(left)
right_bits = extract_lsb(right)

# Convertir bits en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return bytes(result)

left_bytes = bits_to_bytes(left_bits)
right_bytes = bits_to_bytes(right_bits)

print("Left bytes (first 200):")
print(left_bytes[:200])

print("\nRight bytes (first 200):")
print(right_bytes[:200])

# Chercher des caractères imprimables
def printable_only(data):
    return ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)

print("\nLeft printable (first 300):")
print(printable_only(left_bytes[:300]))

print("\nRight printable (first 300):")
print(printable_only(right_bytes[:300]))