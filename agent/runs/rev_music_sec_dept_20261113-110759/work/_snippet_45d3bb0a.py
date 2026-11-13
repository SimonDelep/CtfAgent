# Analyser la structure complète
with open('session.bin', 'rb') as f:
    data = f.read()

# Chercher les motifs 0x80 et 0x81
print("Analyse des marqueurs 0x80 et 0x81:")

# 0x80 XX
pairs_80 = []
for i in range(len(data)-1):
    if data[i] == 0x80:
        pairs_80.append((i, data[i+1]))

print(f"\nNombre d'occurrences de 0x80: {len(pairs_80)}")
print("Premières paires (0x80, valeur_suivante):")
for pos, val in pairs_80[:20]:
    print(f"  Pos {pos}: 0x80 0x{val:02x} ({val})")

# Décoder tout le fichier en traitant 0x80 et 0x81 comme des marqueurs
def decode_file(data):
    result = []
    i = 0
    while i < len(data):
        if data[i] == 0x81 and i+1 < len(data):
            # 0x81 XX -> caractère
            val = data[i+1]
            if 32 <= val < 127:
                result.append(chr(val))
            else:
                result.append(f'[{val:02x}]')
            i += 2
        elif data[i] == 0x80 and i+1 < len(data):
            # 0x80 XX -> peut-être un autre type de caractère ou marqueur
            val = data[i+1]
            if 32 <= val < 127:
                result.append(chr(val))
            else:
                result.append(f'<{val:02x}>')
            i += 2
        else:
            # Autres octets
            if data[i] >= 32 and data[i] < 127:
                result.append(chr(data[i]))
            else:
                result.append(f'.{data[i]:02x}.')
            i += 1
    return ''.join(result)

decoded = decode_file(data)
print("\nFichier décodé (premier millier de caractères):")
print(decoded[:1000])