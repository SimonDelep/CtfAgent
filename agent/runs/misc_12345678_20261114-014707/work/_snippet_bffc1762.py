import base64
import re

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher directement "csaw" ou "flag" dans le fichier brut
print("Recherche de 'csaw' dans le fichier brut:")
idx = data.find(b'csaw')
print(f"  Position: {idx}")
if idx >= 0:
    print(f"  Contexte: {data[idx:idx+20]}")

print("\nRecherche de 'flag' dans le fichier brut:")
idx = data.find(b'flag')
print(f"  Position: {idx}")
if idx >= 0:
    print(f"  Contexte: {data[idx:idx+20]}")

# Chercher dans les métadonnées ID3
# L'ID3 commence à la position 6064294 selon l'analyse précédente
id3_start = 6064294
if id3_start < len(data):
    id3_data = data[id3_start:id3_start+200]
    print(f"\nDonnées ID3 (premier 200 octets):")
    print(id3_data[:100])
    
# Chercher les métadonnées LIST INFO
# LIST INFO est avant ID3
print("\nRecherche de 'LIST' dans le fichier:")
idx = data.find(b'LIST')
print(f"  Position: {idx}")
if idx >= 0:
    print(f"  Contexte: {data[idx:idx+50]}")

# Chercher 'ICRD' qui est la frame de date
idx = data.find(b'ICRD')
print(f"\nPosition de 'ICRD': {idx}")
if idx >= 0:
    print(f"  Contexte: {data[idx:idx+50]}")