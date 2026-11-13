with open('session.bin', 'rb') as f:
    data = f.read()

# Le motif 0x81-encoded "flag{" est à position 124
# 0x81 XX où XX est le caractère ASCII
# Donc "flag{" encodé serait: 81 66 81 6c 81 61 81 67 81 7b

# Trouvons la position exacte
pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
flag_start = data.find(pattern)
print(f"Position du motif 'flag{{' encodé: {flag_start}")

# Après le motif, il y a probablement un saut de ligne ou autre
# Regardons les octets après le motif
print(f"\nOctets après le motif (positions {flag_start} à {flag_start+30}):")
print(data[flag_start:flag_start+30].hex())
print(data[flag_start:flag_start+30])

# Le motif fait 10 octets (5 caractères * 2 octets chacun)
# Après le motif, cherchons où commence le contenu chiffré
after_flag = data[flag_start+10:]
print(f"\nAprès le motif 'flag{{' (10 octets):")
print(after_flag[:50].hex())
print(after_flag[:50])