import struct

with open('catalog.db-wal', 'rb') as f:
    data = f.read()

page_size = 1024

# Regarder la frame 0 en détail
offset = 32
page_data = data[offset+8:offset+8+page_size]

# Chercher le pattern 23010300
pattern = b'\x23\x01\x03\x00'
pos = page_data.find(pattern)
print(f"Position du pattern 23010300: {pos}")

if pos >= 0:
    # Extraire 32 octets à partir de cette position
    share = page_data[pos:pos+32]
    print(f"Share à partir de {pos}: {share.hex()}")
    
    # Le share est probablement les 28 octets après le header
    share_body = page_data[pos+4:pos+32]
    print(f"Body du share (28 octets): {share_body.hex()}")