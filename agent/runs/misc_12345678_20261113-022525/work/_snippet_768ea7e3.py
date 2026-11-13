import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
data_start = data.find(b'data')
audio_data = data[data_start+8:data_start+8+6064208]

# Extraire les LSB de chaque échantillon (1 bit par échantillon)
# C'est stéréo, donc on a 2 canaux
bits = []
for i in range(0, len(audio_data), 4):
    if i + 3 < len(audio_data):
        left = struct.unpack('<h', audio_data[i:i+2])[0]
        right = struct.unpack('<h', audio_data[i+2:i+4])[0]
        bits.append(left & 1)
        bits.append(right & 1)

print(f"Nombre de bits extraits: {len(bits)}")

# Convertir en bytes
bytes_data = []
for i in range(0, len(bits) - 7, 8):
    byte_val = 0
    for j in range(8):
        byte_val |= (bits[i+j] << j)
    bytes_data.append(byte_val)

print(f"Nombre de bytes: {len(bytes_data)}")

# Afficher les premiers bytes en hex et en ASCII
print("\nPremiers 100 bytes (hex):")
print(' '.join(f'{b:02x}' for b in bytes_data[:100]))

print("\nPremiers 100 bytes (ASCII):")
printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_data[:100])
print(printable)

# Chercher "csaw{" ou "flag"
text = ''.join(chr(b) if 32 <= b < 127 else '' for b in bytes_data)
print("\nTexte lisible trouvé:")
print(text[:200])