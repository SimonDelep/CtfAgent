import wave

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    data = wav.readframes(wav.getnframes())

# Peut-être que le flag est encodé dans les valeurs des échantillons eux-mêmes
# Ou peut-être que c'est un encodage ASCII des valeurs

# Essayons de chercher "csaw" en cherchant les codes ASCII correspondants
# 'c' = 99, 's' = 115, 'a' = 97, 'w' = 119

# Chercher la séquence 99, 115, 97, 119 dans les données
target = [99, 115, 97, 119]
for i in range(len(data) - 4):
    if list(data[i:i+4]) == target:
        print(f"Séquence 'csaw' trouvée à l'offset {i}")
        print(f"Contexte: {data[i:i+20]}")
        break
else:
    print("'csaw' pas trouvé comme séquence de bytes")

# Peut-être que c'est en little-endian ou big-endian
# Ou peut-être que c'est dans les échantillons 16-bit

# Convertir les données en échantillons 16-bit
import struct
samples = struct.unpack('<' + 'h' * (len(data) // 2), data)

# Chercher "csaw" dans les échantillons
for i in range(len(samples) - 4):
    if list(samples[i:i+4]) == target:
        print(f"Séquence 'csaw' trouvée dans les échantillons à l'index {i}")
        break
else:
    print("'csaw' pas trouvé dans les échantillons 16-bit")

# Autre idée: peut-être que "12345678" est le flag lui-même?
# Ou peut-être que c'est un mot de passe pour décoder

# Essayons de chercher des motifs binaires
# "csaw{" en binaire: c=01100011, s=01110011, a=01100001, w=01110111, {=01111011

print("\n--- Recherche de motifs binaires ---")
# Extraire tous les bits
all_bits = []
for byte in data:
    for bit in range(7, -1, -1):
        all_bits.append((byte >> bit) & 1)

# Chercher "csaw{" en binaire
csaw_binary = []
for char in "csaw{":
    for bit in range(7, -1, -1):
        csaw_binary.append((ord(char) >> bit) & 1)

print(f"Motif 'csaw{{' en binaire: {''.join(map(str, csaw_binary))}")

# Chercher ce motif dans les bits
pattern = ''.join(map(str, csaw_binary))
bits_str = ''.join(map(str, all_bits))
idx = bits_str.find(pattern)
if idx != -1:
    print(f"Motif trouvé à l'index bit {idx}")
else:
    print("Motif 'csaw{' pas trouvé en binaire direct")
