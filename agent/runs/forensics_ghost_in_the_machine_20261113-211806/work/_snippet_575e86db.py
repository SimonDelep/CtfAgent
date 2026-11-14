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
paquets_info = []

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
    port_dst = struct.unpack('>H', data[udp_start+2:udp_start+4])[0]
    
    ports_sources_ordered.append(port_src)
    paquets_info.append({
        'port_src': port_src,
        'port_dst': port_dst
    })
    
    i += 2

# Identifier les singletons
port_counts = Counter(ports_sources_ordered)
singleton_ports = {p for p, c in port_counts.items() if c == 1}

# Extraire les ports singletons dans l'ordre d'apparition
singleton_ordered = [p for p in ports_sources_ordered if p in singleton_ports]

print(f"Nombre de singletons: {len(singleton_ordered)}")
print(f"Premiers 20 singletons dans l'ordre: {singleton_ordered[:20]}")

# La clé est "sh4dow" (6 caractères)
key = "sh4dow"
key_bytes = [ord(c) for c in key]
print(f"Clé: {key}")
print(f"Clé en bytes: {key_bytes}")

# XOR les singletons avec la clé
# Les ports singletons sont autour de 50000, donc on prend port % 256
result = []
for i, port in enumerate(singleton_ordered):
    port_byte = port % 256
    key_byte = key_bytes[i % len(key_bytes)]
    decrypted_byte = port_byte ^ key_byte
    result.append(decrypted_byte)

print(f"\nRésultat XOR (bytes): {result[:30]}")
print(f"Résultat XOR (chars): {''.join(chr(b) if 32 <= b < 127 else '?' for b in result[:30])}")

# Essayer de convertir tout le résultat en string
decrypted = bytes(result)
print(f"\nDécrypté complet (bytes): {decrypted[:50]}")
print(f"Décrypté complet (string): {decrypted.decode('latin-1')[:50]}")