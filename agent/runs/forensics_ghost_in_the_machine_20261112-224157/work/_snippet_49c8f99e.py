import struct

# Lire le fichier pcap
with open('capture_fixed.pcap', 'rb') as f:
    data = f.read()

# Parser tous les paquets
offset = 24
packets = []

while offset < len(data):
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    if incl_len == 0 or incl_len > 1000:
        break
    packet_data = data[offset+16:offset+16+incl_len]
    packets.append(packet_data)
    offset += 16 + incl_len

# Afficher la structure complète d'un paquet
pkt = packets[0]
print("Structure d'un paquet (46 octets):")
for i in range(0, len(pkt), 8):
    chunk = pkt[i:i+8]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    print(f"  {i:3d}: {hex_str:24s}  {ascii_str}")

print("\n\nComparaison entre deux paquets différents:")
# Trouver deux paquets qui diffèrent
for i in range(len(packets)):
    for j in range(i+1, len(packets)):
        if packets[i] != packets[j]:
            print(f"Paquet {i} vs Paquet {j}:")
            for k in range(len(packets[i])):
                if packets[i][k] != packets[j][k]:
                    print(f"  Position {k}: {packets[i][k]:02x} vs {packets[j][k]:02x}")
            break
    else:
        continue
    break