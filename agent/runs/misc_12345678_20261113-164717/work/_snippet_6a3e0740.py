import struct

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouver le chunk 'data'
idx = data.find(b'data')
data_size = struct.unpack('<I', data[idx+4:idx+8])[0]
audio_data = data[idx+8:idx+8+data_size]

# Extraire LSB de chaque échantillon (chaque échantillon est 2 octets)
# On va extraire le bit LSB de chaque échantillon
bits = []
for i in range(0, len(audio_data), 2):
    if i+1 < len(audio_data):
        sample = struct.unpack('<h', audio_data[i:i+2])[0]
        bits.append(sample & 1)

print(f"Nombre de bits: {len(bits)}")

# Convertir en bytes
bytes_data = []
for i in range(0, len(bits), 8):
    if i+7 < len(bits):
        byte_val = 0
        for j in range(8):
            byte_val |= (bits[i+j] << j)
        bytes_data.append(byte_val)

print(f"Nombre de bytes: {len(bytes_data)}")

# Afficher les premiers bytes en hex et en ASCII
print("Premiers bytes (hex):", bytes(bytes_data[:100]).hex())
print("Premiers bytes (ASCII):", bytes(bytes_data[:100]))

# Essayer de trouver du texte lisible
text = bytes(bytes_data)
# Chercher des patterns ASCII
print("\nRecherche de texte ASCII:")
for i in range(len(text)-10):
    chunk = text[i:i+20]
    try:
        decoded = chunk.decode('ascii')
        if decoded.isprintable():
            print(f"Position {i}: {decoded}")
    except:
        pass