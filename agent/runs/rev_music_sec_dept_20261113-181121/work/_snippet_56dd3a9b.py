# Analyser plus en détail
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher toutes les occurrences de 0x81
positions = []
for i, b in enumerate(data):
    if b == 0x81:
        positions.append(i)

print(f"Nombre d'occurrences de 0x81: {len(positions)}")
print(f"Positions: {positions[:20]}")

# Extraire les paires 0x81xx
pairs = []
for i in positions:
    if i+1 < len(data):
        pairs.append((i, data[i+1]))

# Afficher les paires
print("\nPaires 0x81xx:")
for pos, val in pairs[:30]:
    char = chr(val) if 32 <= val < 127 else f'[{val}]'
    print(f"  {pos}: 0x81 0x{val:02x} = {char}")