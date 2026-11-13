# Cherchons la chaîne chiffrée complète dans le fichier MP4
with open('finderskeepers.mp4', 'rb') as f:
    data = f.read()

# Cherchons "esnp{" ou "csaw{"
esnp_brace = data.find(b'esnp{')
if esnp_brace != -1:
    print(f"Trouvé 'esnp{{' à la position {esnp_brace}")
    # Trouver la fin de la chaîne (chercher '}')
    end_brace = data.find(b'}', esnp_brace)
    if end_brace != -1:
        cipher = data[esnp_brace:end_brace+1]
        print(f"Chaîne chiffrée: {cipher.decode('utf-8', errors='ignore')}")
else:
    print("'esnp{' non trouvé")
    # Cherchons "csaw{"
    csaw_brace = data.find(b'csaw{')
    if csaw_brace != -1:
        print(f"Trouvé 'csaw{{' à la position {csaw_brace}")
        end_brace = data.find(b'}', csaw_brace)
        if end_brace != -1:
            flag = data[csaw_brace:end_brace+1]
            print(f"Flag: {flag.decode('utf-8', errors='ignore')}")

# Cherchons aussi des chaînes contenant "@"
at_positions = []
pos = 0
while True:
    pos = data.find(b'@', pos)
    if pos == -1:
        break
    at_positions.append(pos)
    pos += 1

print(f"\nPositions de '@': {at_positions[:10]}")

# Pour chaque position de '@', affichons le contexte
for pos in at_positions[:5]:
    print(f"\nContexte autour de '@' à {pos}:")
    print(data[pos-20:pos+30])