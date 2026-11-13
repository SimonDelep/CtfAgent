import wave
import struct
from collections import Counter

# Lire le fichier WAV
with wave.open('audio.wav', 'rb') as wav:
    raw_data = wav.readframes(wav.getnframes())
    samples = struct.unpack(f'{wav.getnframes() * wav.getnchannels()}h', raw_data)

# Filtrer seulement les valeurs dont la valeur absolue est entre 1 et 8
filtered = [s for s in samples if 1 <= abs(s) <= 8]

# Approche: utiliser la valeur absolue comme index et le signe comme bit
# Par exemple, +1 = 0001, -1 = 1001, +2 = 0010, -2 = 1010, etc.
# Ou peut-être que c'est plus simple: signe = bit de poids fort, valeur = 4 bits

# Autre idée: peut-être que c'est un encodage où chaque paire (signe, valeur) donne un caractère
# 16 symboles = 4 bits par symbole

# Créons une séquence de 4 bits par symbole
# +1 = 0000, -1 = 0001, +2 = 0010, -2 = 0011, +3 = 0100, -3 = 0101, etc.
def sym_to_bits(s):
    abs_val = abs(s)
    is_neg = 1 if s < 0 else 0
    # Mapping: +1=0, -1=1, +2=2, -2=3, +3=4, -3=5, +4=6, -4=7, +5=8, -5=9, +6=10, -6=11, +7=12, -7=13, +8=14, -8=15
    idx = (abs_val - 1) * 2 + is_neg
    return idx

# Convertir les premiers symboles en indices
indices = [sym_to_bits(s) for s in filtered[:100]]
print("Indices des premiers symboles:")
print(indices[:50])

# Regrouper par 4 indices pour former un byte (4 * 4 = 16 bits = 2 bytes)
# Ou regrouper par 2 indices pour former un byte (2 * 4 = 8 bits)
bytes_from_pairs = []
for i in range(0, len(indices) - 1, 2):
    byte_val = indices[i] * 16 + indices[i+1]
    bytes_from_pairs.append(byte_val)

print("\nPremiers bytes (groupés par 2):")
print(bytes_from_pairs[:50])

# Convertir en caractères imprimables
chars = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_from_pairs[:100])
print(f"\nCaractères: {chars}")
