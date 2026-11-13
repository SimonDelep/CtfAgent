import struct

# Lire le fichier pcap
with open('capture_fixed.pcap', 'rb') as f:
    data = f.read()

# Parser tous les paquets
offset = 24  # Après le header global
packets = []

while offset < len(data):
    if offset + 16 > len(data):
        break
    
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    
    if incl_len == 0 or incl_len > 1000:
        break
    
    packet_data = data[offset+16:offset+16+incl_len]
    packets.append({
        'ts_sec': ts_sec,
        'ts_usec': ts_usec,
        'data': packet_data
    })
    
    offset += 16 + incl_len

print(f"Total paquets: {len(packets)}")

# Analyser les variations dans les données des paquets
# Chaque paquet a 46 octets
# Regardons les différences entre paquets

# Extraire chaque octet position sur tous les paquets
positions = {}
for i, pkt in enumerate(packets):
    for j, byte in enumerate(pkt['data']):
        if j not in positions:
            positions[j] = []
        positions[j].append(byte)

# Trouver les positions qui varient
varying_positions = {}
for pos, bytes_list in positions.items():
    unique_bytes = set(bytes_list)
    if len(unique_bytes) > 1:
        varying_positions[pos] = unique_bytes

print(f"\nPositions variables (avec valeurs uniques):")
for pos in sorted(varying_positions.keys()):
    print(f"  Position {pos}: {len(varying_positions[pos])} valeurs uniques - {sorted(varying_positions[pos])[:10]}...")

# Regardons les positions 8, 9, 10 mentionnées dans le résumé
print("\n\nValeurs aux positions 8, 9, 10 sur les 10 premiers paquets:")
for i in range(10):
    pkt_data = packets[i]['data']
    if len(pkt_data) > 10:
        print(f"Paquet {i}: pos8={pkt_data[8]:02x}({chr(pkt_data[8]) if 32<=pkt_data[8]<127 else '?'}), pos9={pkt_data[9]:02x}({chr(pkt_data[9]) if 32<=pkt_data[9]<127 else '?'}), pos10={pkt_data[10]:02x}({chr(pkt_data[10]) if 32<=pkt_data[10]<127 else '?'})")