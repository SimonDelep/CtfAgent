import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024

# Regarder la frame 0 en détail
offset = 32
page_data = data[offset+8:offset+8+page_size]

# Afficher les derniers octets de la page
print(f"Derniers 50 octets de la page: {page_data[-50:].hex()}")
print(f"Taille de page_data: {len(page_data)}")

# Chercher le pattern 23010300
pattern = b'\x23\x01\x03\x00'
pos = page_data.find(pattern)
print(f"Position du pattern: {pos}")

if pos >= 0:
    # Extraire jusqu'à la fin de la page
    remaining = len(page_data) - pos
    print(f"Octets restants après le pattern: {remaining}")
    print(f"Données: {page_data[pos:].hex()}")