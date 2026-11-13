# Regardons la fin du fichier et cherchons des patterns
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

print("Taille du fichier:", len(data))
print("Derniers 200 octets:")
print(data[-200:].hex())
print()
print("Derniers 200 octets (brut):")
print(data[-200:])

# Chercher "}" en cherchant 0x7d
for i, b in enumerate(data):
    if b == 0x7d:
        print(f"Trouve 0x7d a la position {i}")

# Chercher 0x81 suivi de quelque chose qui pourrait être '}'
# 0x7d = 125, donc cherchons 0x81 0x7d
for i in range(len(data)-1):
    if data[i] == 0x81:
        next_byte = data[i+1]
        if next_byte == 0x7d:
            print(f"Trouve 0x81 0x7d a la position {i}")
        # Afficher les 0x81 avec des valeurs proches de 0x7d
        if 0x70 <= next_byte <= 0x80:
            print(f"0x81 0x{next_byte:02x} a la position {i} (char: {chr(next_byte) if 32 <= next_byte < 127 else '?'})")