import wave

with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Essayer LSB sur les bytes pairs seulement
lsb_even = [data[i] & 1 for i in range(0, len(data), 2)]
lsb_odd = [data[i] & 1 for i in range(1, len(data), 2)]

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte_val = 0
        for j in range(8):
            byte_val |= (bits[i + j] << (7 - j))
        result.append(byte_val)
    return result

even_bytes = bits_to_bytes(lsb_even)
odd_bytes = bits_to_bytes(lsb_odd)

print("LSB bytes pairs:")
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in even_bytes[:200]))
print()
print("LSB bytes impairs:")
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in odd_bytes[:200]))