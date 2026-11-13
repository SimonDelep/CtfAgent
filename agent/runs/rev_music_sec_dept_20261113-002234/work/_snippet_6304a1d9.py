# Analyser session.bin pour décoder les séquences 0x81XX
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher les séquences 0x81 suivies d'un octet
result = []
i = 0
while i < len(data) - 1:
    if data[i] == 0x81:
        result.append((i, data[i+1]))
    i += 1

# Afficher les premières séquences
print("Séquences 0x81XX trouvées:")
for pos, val in result[:50]:
    print(f"  Pos {pos}: 0x81 0x{val:02x} = {val} (char: {chr(val) if 32 <= val < 127 else '?'})")

# Essayer de décoder tout le fichier en remplaçant 0x81XX par le caractère
decoded = bytearray()
i = 0
while i < len(data):
    if data[i] == 0x81 and i + 1 < len(data):
        decoded.append(data[i+1])
        i += 2
    else:
        decoded.append(data[i])
        i += 1

print("\n--- Contenu décodé (premier 500 octets) ---")
print(decoded[:500].decode('latin-1', errors='replace'))