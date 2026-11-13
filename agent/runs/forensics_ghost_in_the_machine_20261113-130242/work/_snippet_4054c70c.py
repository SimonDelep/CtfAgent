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

# Collecter les IP checksums et ports pour tous les paquets
packets_info = []

for i in range(0, len(positions), 2):
    start = positions[i]
    if start + 54 >= len(data):
        break
    
    src_port = struct.unpack('>H', data[start+34:start+36])[0]
    ip_checksum = struct.unpack('>H', data[start+24:start+26])[0]
    
    packets_info.append((i//2, src_port, ip_checksum))

# Trouver les singletons (ports uniques)
port_counts = Counter([p[1] for p in packets_info])
singletons = [(idx, port, ip_cksum) for idx, port, ip_cksum in packets_info if port_counts[port] == 1]

# Les ports fréquents (bruit)
frequent = [(idx, port, ip_cksum) for idx, port, ip_cksum in packets_info if port_counts[port] > 1]

print(f"Singletons: {len(singletons)}")
print(f"Paquets fréquents: {len(frequent)}")

# Vérifier les IP checksums pour les singletons vs fréquents
singleton_ip_cksums = [p[2] for p in singletons]
frequent_ip_cksums = [p[2] for p in frequent]

print(f"\nIP checksums pour singletons: {set(singleton_ip_cksums)}")
print(f"IP checksums pour fréquents: {set(frequent_ip_cksums)}")

# Trier les singletons par ordre d'apparition
singletons_sorted = sorted(singletons, key=lambda x: x[0])

# Extraire les ports singletons
singleton_ports = [p[1] for p in singletons_sorted]

# Peut-être que le message est dans les ports singletons, mais il faut les décoder
# Regardons si les ports singletons ont un pattern

# Essayer de convertir les ports en bytes
print("\nPorts singletons en bytes:")
for i, p in enumerate(singleton_ports[:20]):
    high = (p >> 8) & 0xff
    low = p & 0xff
    print(f"  {i}: {p} -> bytes: {high:02x} {low:02x}")

# Peut-être que le message est encodé dans les low bytes seulement?
low_bytes = [p & 0xff for p in singleton_ports]
print("\nLow bytes des ports singletons:")
print(low_bytes[:30])

# Essayer de convertir en ASCII
ascii_chars = [chr(b) if 32 <= b < 127 else '?' for b in low_bytes]
print("\nASCII des low bytes:")
print(''.join(ascii_chars[:50]))