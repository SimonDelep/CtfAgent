with open('session.bin', 'rb') as f:
    data = f.read()

# Position du motif 'flag{' encodé
flag_start = 124

# Après le motif 'flag{' (10 octets), on a:
# 81 0a = '\n' encodé
# 02 00 00 00 = en-tête
# Puis les données chiffrées

# Trouvons où commence la clé s4lt26
key_pos = data.find(b's4lt26')
print(f"Position de 's4lt26': {key_pos}")

# Les données chiffrées sont entre la fin de l'en-tête et le début de la clé
# L'en-tête est à flag_start + 10 + 2 (pour 81 0a) + 4 (pour 02 00 00 00) = flag_start + 16
header_end = flag_start + 10 + 2 + 4
print(f"Fin de l'en-tête: {header_end}")

# Données chiffrées
encrypted = data[header_end:key_pos]
print(f"Longueur des données chiffrées: {len(encrypted)}")
print(f"Données chiffrées (hex): {encrypted.hex()}")

# La clé est "s4lt26"
key = b's4lt26'

# Décrypter par XOR
decrypted = []
for i, b in enumerate(encrypted):
    decrypted.append(b ^ key[i % len(key)])

print(f"\nDécrypté: {bytes(decrypted)}")