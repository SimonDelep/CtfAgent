# Analyser session.bin pour extraire le flag
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher la séquence flag{
idx = data.find(b'flag{')
print(f"Index de 'flag': {idx}")

# Regardons autour de l'offset 0x80
print("\nDonnees autour de 0x80:")
for i in range(0x78, 0xb0):
    c = chr(data[i]) if 32 <= data[i] < 127 else '.'
    print(f"{i:04x}: {data[i]:02x} ({c})")

# Cherchons le motif 81 XX qui pourrait etre un encodage
print("\nRecherche de motif 81 XX:")
for i in range(len(data)-1):
    if data[i] == 0x81:
        c = chr(data[i+1]) if 32 <= data[i+1] < 127 else '.'
        print(f"Offset {i:04x}: 81 {data[i+1]:02x} = '{c}'")