import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    data = f.read()

marker = b'\xde\xad\xbe\xef'

# Trouver toutes les positions des marqueurs
positions = []
pos = 0
while True:
    idx = data.find(marker, pos)
    if idx == -1:
        break
    positions.append(idx)
    pos = idx + 1

# Extraire les ports sources dans l'ordre
ports_sources_ordered = []

i = 0
while i < len(positions) - 1:
    marker1_pos = positions[i]
    marker2_pos = positions[i+1]
    
    ip_start = data.find(b'\x45\x00', marker2_pos)
    if ip_start == -1:
        i += 2
        continue
    
    udp_start = ip_start + 20
    
    if udp_start + 8 > len(data):
        break
    
    port_src = struct.unpack('>H', data[udp_start:udp_start+2])[0]
    ports_sources_ordered.append(port_src)
    i += 2

# Identifier les singletons
port_counts = Counter(ports_sources_ordered)
singleton_ports = {p for p, c in port_counts.items() if c == 1}

# Extraire les ports singletons dans l'ordre d'apparition
singleton_ordered = [p for p in ports_sources_ordered if p in singleton_ports]

# Essayer avec tri par valeur
singleton_sorted = sorted(singleton_ports)

print(f"Singletons triés par valeur (premiers 20): {singleton_sorted[:20]}")

# Clé "sh4dow"
key = "sh4dow"
key_bytes = [ord(c) for c in key]

# Essayer XOR avec les singletons triés par valeur
result_sorted = []
for i, port in enumerate(singleton_sorted):
    port_byte = port % 256
    key_byte = key_bytes[i % len(key_bytes)]
    decrypted_byte = port_byte ^ key_byte
    result_sorted.append(decrypted_byte)

print(f"\nRésultat XOR (trié par valeur):")
print(f"Bytes: {result_sorted[:30]}")
print(f"Chars: {''.join(chr(b) if 32 <= b < 127 else '?' for b in result_sorted[:50])}")

# Vérifier si le résultat commence par "csaw{"
decrypted_sorted = bytes(result_sorted)
print(f"\nDécrypté (trié): {decrypted_sorted[:20]}")

# Essayer de trouver un préfixe de flag
for start in range(len(result_sorted) - 4):
    chunk = result_sorted[start:start+5]
    if chunk == [99, 115, 97, 119, 123]:  # "csaw{"
        print(f"Trouvé 'csaw{'{' }' à la position {start}")
        break