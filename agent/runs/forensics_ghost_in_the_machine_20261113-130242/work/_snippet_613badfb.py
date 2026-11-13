import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Trouver tous les marqueurs dead beef
marker = bytes.fromhex('deadbeef')
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Collecter les ports source et leurs timestamps
# On a besoin de l'ordre d'apparition (timestamp)
# Le timestamp est probablement stocké quelque part dans le paquet

# Regardons la structure complète d'un paquet
start = positions[0]
print("Structure complète d'un paquet:")
chunk = data[start:start+62]
for i in range(0, len(chunk), 16):
    hex_part = chunk[i:i+16].hex()
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk[i:i+16])
    print(f"  {start+i:04x}: {hex_part:<32} {ascii_part}")

# Cherchons où sont stockés les timestamps
# Peut-être après le payload?
print("\nRegardons ce qui suit le payload 'PING':")
# PING est à offset 42-45 (0x50494e47)
# Après PING, il y a 00f1 5365
print(f"Bytes après PING: {chunk[46:54].hex()}")