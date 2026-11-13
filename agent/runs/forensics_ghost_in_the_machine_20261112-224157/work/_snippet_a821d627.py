import struct

# Lire le PCAP et analyser la structure
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Vérifier le magic header
magic = struct.unpack('<I', data[:4])[0]
print(f"Magic header: 0x{magic:08x}")

# Si c'est 0xa1b2c3d4, c'est un format microsecondes
# Si c'est 0xd4c3b2a1, c'est le format standard (bytes swapped)

# Parse le header global
if magic == 0xa1b2c3d4:
    print("Format: microsecondes")
    header_size = 24
elif magic == 0xd4c3b2a1:
    print("Format: standard (bytes swapped)")
    header_size = 24
else:
    print(f"Magic inconnu: 0x{magic:08x}")
    header_size = 24

# Parse les paquets
offset = header_size
packets = []
while offset < len(data):
    # Header du paquet: ts_sec, ts_usec, incl_len, orig_len
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append((ts_sec, ts_usec, pkt_data))

print(f"Nombre de paquets: {len(packets)}")

# Analyser la structure des paquets
# On s'attend à voir un marqueur deadbeef
for i, (ts, usec, pkt) in enumerate(packets[:5]):
    print(f"Paquet {i}: len={len(pkt)}, hex={pkt[:20].hex()}")