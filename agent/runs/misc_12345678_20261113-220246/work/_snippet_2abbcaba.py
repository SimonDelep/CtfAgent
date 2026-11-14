import struct

with open('audio.wav', 'rb') as f:
    data = f.read()

# Le chunk ID3 est à offset 6064286, taille 46
id3_start = 6064286
id3_size = 46

id3_data = data[id3_start+8:id3_start+8+id3_size]
print(f"Chunk ID3 contenu ({len(id3_data)} octets):")
print(id3_data)
print()
print("En hex:")
print(id3_data.hex())

# Essayer de décoder comme texte
try:
    print("\nEn texte:")
    print(id3_data.decode('utf-8', errors='replace'))
except:
    pass