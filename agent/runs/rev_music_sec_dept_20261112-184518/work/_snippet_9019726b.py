# Analyser la structure de session.bin
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Trouver la position de flag{
idx = data.find(b'\x81\x66\x81\x6c\x81\x61\x81\x67\x81\x7b')  # flag{ encodé
print(f"Position de 'flag{{': {idx} (0x{idx:x})")

# Après flag{, on a 81 0a 02 00 00 00 puis les données chiffrées
# Cherchons le motif s4lt26
salt_pos = data.find(b's4lt26')
print(f"Position de 's4lt26': {salt_pos} (0x{salt_pos:x})")

# Cherchons M4ch1n3_K3y!!
key_pos = data.find(b'M4ch1n3_K3y!!')
print(f"Position de 'M4ch1n3_K3y!!': {key_pos} (0x{key_pos:x})")

# Regardons les données après flag{
print("\nDonnées après flag{ (offset 0x86):")
start = idx + 8  # après flag{
for i in range(start, min(start + 64, len(data))):
    print(f"{i:04x}: {data[i]:02x}")

# Essayons de décoder avec XOR en utilisant le salt
# Le flag semble commencer après les 6 octets de contrôle (81 0a 02 00 00 00)
# Donc le flag chiffré commence à offset 0x8c

print("\nDonnées chiffrées (à partir de 0x8c):")
cipher_start = 0x8c
for i in range(cipher_start, min(cipher_start + 48, len(data))):
    print(f"{i:04x}: {data[i]:02x} ({chr(data[i]) if 32 <= data[i] < 127 else '.'})")