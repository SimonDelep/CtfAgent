# Chercher "ID3" partout dans le fichier
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher toutes les occurrences de "ID3"
import re
matches = list(re.finditer(rb'ID3', data))
print(f"Nombre d'occurrences de 'ID3': {len(matches)}")
for m in matches:
    pos = m.start()
    print(f"  Position {pos}: {data[pos:pos+20]}")

# Chercher aussi "LIST"
matches_list = list(re.finditer(rb'LIST', data))
print(f"\nNombre d'occurrences de 'LIST': {len(matches_list)}")
for m in matches_list:
    pos = m.start()
    print(f"  Position {pos}: {data[pos:pos+20]}")