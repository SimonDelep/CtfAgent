# Lisons l'en-tête du fichier WAV manuellement
with open('audio.wav', 'rb') as f:
    data = f.read()

print(f"Total file size: {len(data)} bytes")

# En-tête WAV
print(f"First 44 bytes (WAV header):")
print(data[:44].hex())

# Chercher des chaînes imprimables dans tout le fichier
import re

# Extraire toutes les séquences imprimables de longueur >= 4
text = data.decode('latin-1')
sequences = re.findall(r'[\x20-\x7e]{4,}', text)

print(f"\nPrintable sequences in file (min 4 chars):")
for seq in sequences[:50]:
    print(repr(seq))