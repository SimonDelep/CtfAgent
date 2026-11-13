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

# Collecter les ports source et after_ping pour tous les paquets
packets_info = []

for i in range(0, len(positions), 2):
    start = positions[i]
    if start + 54 >= len(data):
        break
    
    src_port = struct.unpack('>H', data[start+34:start+36])[0]
    after_ping = data[start+46:start+54]
    
    packets_info.append((i//2, src_port, after_ping))

# Trouver les singletons
port_counts = Counter([p[1] for p in packets_info])
singletons = [(idx, port, after_ping) for idx, port, after_ping in packets_info if port_counts[port] == 1]

# Trier par ordre d'apparition
singletons_sorted = sorted(singletons, key=lambda x: x[0])

# Extraire les ports singletons
singleton_ports = [p[1] for p in singletons_sorted]

# La clé pourrait être "5365" = "Se" ou quelque chose comme ça
# Essayons de XORer les ports avec différentes clés

# Option 1: XOR avec 0x5365
key1 = 0x5365
decoded1 = [chr((p ^ key1) % 256) if 32 <= (p ^ key1) % 256 < 127 else '?' for p in singleton_ports]
print("XOR avec 0x5365:")
print(''.join(decoded1[:30]))

# Option 2: XOR avec le port modulo 256
decoded2 = [chr(p % 256) if 32 <= p % 256 < 127 else '?' for p in singleton_ports]
print("\nPort mod 256:")
print(''.join(decoded2[:30]))

# Option 3: Peut-être que le port contient le message directement
# Les ports sont autour de 50000, donc peut-être qu'on doit soustraire quelque chose
print("\nPorts - 50000:")
print([p - 50000 for p in singleton_ports[:20]])

# Option 4: Regardons les bytes individuels des ports
print("\nBytes des ports (high byte, low byte):")
for p in singleton_ports[:10]:
    high = (p >> 8) & 0xff
    low = p & 0xff
    print(f"  {p}: high={high} ({chr(high) if 32 <= high < 127 else '?'}), low={low} ({chr(low) if 32 <= low < 127 else '?'})")