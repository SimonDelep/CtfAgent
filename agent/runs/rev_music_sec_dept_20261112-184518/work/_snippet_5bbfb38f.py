with open('session.bin', 'rb') as f:
    data = f.read()

# Afficher les premiers octets en hex
print("Premiers 100 octets:")
print(' '.join(f'{b:02x}' for b in data[:100]))

# Chercher 'flag{' en cherchant le pattern 0x81 + ASCII
# 'f' = 0x66, donc 0x81 + 0x66 = 0xe7
# Mais on voit 'flag{' directement dans le dump, donc peut-être que c'est déjà décodé partiellement

# Trouver l'offset de 'flag{'
idx = data.find(b'flag{')
print(f"\nOffset de 'flag{': {idx}")

# Afficher un peu autour
if idx >= 0:
    print(f"Données autour de 'flag{{':")
    print(' '.join(f'{b:02x}' for b in data[idx:idx+50]))
    print(f"Texte brut: {data[idx:idx+50]}")

# Chercher 's4lt26'
idx_salt = data.find(b's4lt26')
print(f"\nOffset de 's4lt26': {idx_salt}")
if idx_salt >= 0:
    print(f"Données autour de 's4lt26':")
    print(' '.join(f'{b:02x}' for b in data[idx_salt:idx_salt+50]))
