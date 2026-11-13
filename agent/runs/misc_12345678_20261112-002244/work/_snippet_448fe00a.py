import wave
import struct

with wave.open('audio.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames)//2), frames)

# Peut-être que le message est dans les 8 bits de poids faible de chaque sample
# Mais en utilisant seulement certains samples

# Autre idée : peut-être que "12345678" indique qu'il faut prendre les samples
# aux positions 1, 2, 3, 4, 5, 6, 7, 8 (ou 0-indexed: 0, 1, 2, 3, 4, 5, 6, 7)
# et extraire quelque chose de spécifique

# Ou peut-être que c'est une séquence de valeurs à chercher dans les samples

# Essayons de voir si les samples contiennent la séquence 1, 2, 3, 4, 5, 6, 7, 8
# ou des valeurs proches

# Chercher des séquences de samples qui correspondent à des valeurs ASCII
# en utilisant les 8 bits de poids faible

# Peut-être que le message est encodé en modifiant le LSB seulement pour certains samples
# et qu'il faut détecter ces modifications

# Autre approche : peut-être que le message est dans les bits LSB, mais qu'il faut
# le lire en inversant l'ordre des bits ou des bytes

# Essayer de lire les bits LSB en ordre inverse (LSB first vs MSB first)
all_lsb = [s & 1 for s in samples]

# Ordre inverse des bits dans chaque byte
def bits_to_bytes_lsb_first(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte |= bits[i + j] << j  # LSB first
        result.append(byte)
    return bytes(result)

data_lsb_first = bits_to_bytes_lsb_first(all_lsb)

print("LSB first (first 500):")
print(data_lsb_first[:500])

# Chercher "csaw{"
if b'csaw{' in data_lsb_first:
    idx = data_lsb_first.index(b'csaw{')
    print(f"\nFound 'csaw{{' at index {idx}")
    print(data_lsb_first[idx:idx+100])
else:
    if b'{' in data_lsb_first:
        idx = data_lsb_first.index(b'{')
        print(f"\nFound '{{' at index {idx}")
        print(data_lsb_first[max(0,idx-20):idx+40])