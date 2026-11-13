with open('capture.pcap', 'rb') as f:
    data = f.read()

print(f"Taille totale: {len(data)} octets")

# L'en-tête semble être 24 octets
print("\nEn-tête (24 octets):")
print(data[:24].hex())

# Après l'en-tête, on a des blocs de 62 octets (504 paquets)
# 24 + 504*62 = 24 + 31248 = 31272
# Vérifions
print(f"\nTaille attendue: 24 + 504*62 = {24 + 504*62}")

# Analysons la structure d'un bloc
# Cherchons où commence le premier "Se"
se_positions = []
pos = 0
while True:
    pos = data.find(b'Se', pos)
    if pos == -1:
        break
    se_positions.append(pos)
    pos += 1

print(f"\nPositions de 'Se': {se_positions[:10]}")
print(f"Nombre total de 'Se': {len(se_positions)}")

# Regardons ce qui est autour de chaque "Se"
for i, pos in enumerate(se_positions[:5]):
    print(f"\n--- 'Se' à la position {pos} ---")
    print(f"Contexte avant: {data[pos-10:pos]!r}")
    print(f"Contexte après: {data[pos:pos+10]!r}")