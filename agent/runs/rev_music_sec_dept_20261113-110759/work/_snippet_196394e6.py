# Analyser session.bin pour comprendre le format d'encodage
with open('session.bin', 'rb') as f:
    data = f.read()

# Chercher les motifs 0x81
print("Taille du fichier:", len(data))
print("\nPremiers 200 octets en hex:")
print(data[:200].hex())

# Chercher les occurrences de 0x81
positions_81 = [i for i, b in enumerate(data) if b == 0x81]
print(f"\nNombre d'occurrences de 0x81: {len(positions_81)}")

# Regarder les paires 0x81 XX
pairs = []
for i in range(len(data)-1):
    if data[i] == 0x81:
        pairs.append((i, data[i+1]))

print("\nPremières paires (0x81, valeur_suivante):")
for pos, val in pairs[:30]:
    print(f"  Pos {pos}: 0x81 0x{val:02x} ({val})")

# Essayer de décoder: peut-être 0x81 + x = caractère
# Si 0x81 est un préfixe, alors 0x81 + x pourrait encoder un caractère
# Essayons de voir si 0x81 + x = ASCII
decoded = []
i = 0
while i < len(data):
    if data[i] == 0x81 and i+1 < len(data):
        # Peut-être que 0x81 XX encode un caractère
        val = data[i+1]
        # Essayer différentes transformations
        decoded.append((i, val, chr(val) if 32 <= val < 127 else '?'))
        i += 2
    else:
        i += 1

print("\nDécodage simple (0x81 XX -> XX):")
print(''.join([chr(p[1]) if 32 <= p[1] < 127 else '.' for p in pairs[:50]]))