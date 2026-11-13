import struct

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    data = f.read()

offset = 24
packets = []
while offset < len(data):
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append((ts_sec, ts_usec, pkt_data))

# Regardons la structure complète d'un paquet
pkt = packets[0][2]
print("Structure complète d'un paquet (46 octets):")
for i in range(len(pkt)):
    print(f"  [{i:2d}] = {pkt[i]:3d} (0x{pkt[i]:02x}) = {chr(pkt[i]) if 32 <= pkt[i] < 127 else '.'}")

# Comparons deux paquets différents (un État A et un État B)
print("\nComparaison État A vs État B:")
pkt_a = packets[0][2]  # État A
pkt_b = packets[6][2]  # État B

for i in range(len(pkt_a)):
    if pkt_a[i] != pkt_b[i]:
        print(f"  [{i:2d}] A={pkt_a[i]:3d} B={pkt_b[i]:3d} diff={pkt_a[i] ^ pkt_b[i]}")