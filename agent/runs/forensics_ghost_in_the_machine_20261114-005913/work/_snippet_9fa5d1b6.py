import struct
from collections import Counter

# Lire le fichier
with open('capture.pcap', 'rb') as f:
    data = f.read()

deadbeef = b'\xde\xad\xbe\xef'
first_db = data.find(deadbeef)

# Parser les paquets et extraire ports + timestamp (ordre d'apparition)
offset = first_db
packets_info = []
packet_idx = 0
while offset < len(data):
    if data[offset:offset+4] != deadbeef:
        break
    offset += 4  # deadbeef
    offset += 2  # 2 octets
    offset += 4  # deadbeef
    next_db = data.find(deadbeef, offset)
    if next_db == -1:
        packet_data = data[offset:]
        offset = len(data)
    else:
        packet_data = data[offset:next_db]
        offset = next_db
    
    # Extraire port source
    ip_start = packet_data.find(b'\x45\x00')
    if ip_start != -1:
        ihl = packet_data[ip_start] & 0x0F
        ip_header_len = ihl * 4
        src_port_offset = ip_start + ip_header_len
        if src_port_offset + 2 <= len(packet_data):
            src_port = struct.unpack('>H', packet_data[src_port_offset:src_port_offset+2])[0]
            packets_info.append((packet_idx, src_port, packet_data))
            packet_idx += 1

# Compter les fréquences
ports = [p for _, p, _ in packets_info]
freq = Counter(ports)

# Singletons et ports fréquents
singletons = [(idx, p) for idx, p in packets_info if freq[p] == 1]
frequent_ports = [p for p, c in freq.items() if c > 1]

print(f"Singletons (ordre d'apparition): {len(singletons)}")
print(f"Ports fréquents: {frequent_ports}")

# Analyser les ports fréquents pour dériver la clé
print("\nPorts fréquents modulo 256:")
for p in sorted(frequent_ports):
    print(f"  {p} mod 256 = {p % 256} = {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")

# "sh4dow" en ASCII: s=115, h=104, 4=52, d=100, o=111, w=119
print("\nClé 'sh4dow' en ASCII:")
key = "sh4dow"
for c in key:
    print(f"  '{c}' = {ord(c)}")

# Vérifions si les ports fréquents contiennent ces valeurs
print("\nRecherche des valeurs de la clé dans les ports fréquents:")
for c in key:
    val = ord(c)
    found = [p for p in frequent_ports if p % 256 == val]
    print(f"  '{c}' ({val}): {found}")