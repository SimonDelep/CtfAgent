# Lire le binaire
with open('csirac.pd_linux', 'rb') as f:
    data = f.read()

offset = 0xec30
print("Données autour de l'offset 0xec30:")
for i in range(-10, 100):
    pos = offset + i
    if 0 <= pos < len(data):
        byte = data[pos]
        char = chr(byte) if 32 <= byte < 127 else '.'
        print(f"{pos:06x}: {byte:02x} {char}")