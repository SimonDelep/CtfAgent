with open('session.bin', 'rb') as f:
    data = f.read()

# Chercher le motif 0x81 suivi de caractères qui pourraient former "flag{"
# 0x81 0x66 = 'f', 0x81 0x6c = 'l', etc.
# Mais d'abord, voyons où est "flag{" en clair
print("Recherche de 'flag{' en clair:")
idx = data.find(b'flag{')
print(f"  Position: {idx}")

# Cherchons le motif 0x81 suivi de 'f', 'l', 'a', 'g', '{'
# 'f' = 0x66, 'l' = 0x6c, 'a' = 0x61, 'g' = 0x67, '{' = 0x7b
pattern = bytes([0x81, 0x66, 0x81, 0x6c, 0x81, 0x61, 0x81, 0x67, 0x81, 0x7b])
print(f"Recherche du motif 0x81-encoded 'flag{{':")
idx = data.find(pattern)
print(f"  Position: {idx}")

# Affichons les octets autour de la position 176 où on voit "flag{" dans l'affichage
print("\nOctets autour de position 176:")
print(data[170:200].hex())
print(data[170:200])