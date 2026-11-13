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
    udp_checksum = struct.unpack('>H', data[start+40:start+42])[0]
    
    packets_info.append((i//2, src_port, ip_checksum, udp_checksum))

# Vérifier les IP checksums
ip_checksums = [p[2] for p in packets_info]
unique_ip_cksum = set(ip_checksums)
print(f"IP checksums uniques: {unique_ip_cksum}")

# Vérifier les UDP checksums
udp_checksums = [p[3] for p in packets_info]
unique_udp_cksum = set(udp_checksums)
print(f"UDP checksums uniques: {unique_udp_cksum}")

# Regardons les paquets avec des IP checksums différents
non_standard_ip = [(idx, port, ip_cksum, udp_cksum) for idx, port, ip_cksum, udp_cksum in packets_info if ip_cksum != 0xc96e]
print(f"\nPaquets avec IP checksum != 0xc96e: {len(non_standard_ip)}")
for item in non_standard_ip[:10]:
    print(f"  {item}")

# Regardons les paquets avec des UDP checksums non nuls
non_zero_udp = [(idx, port, ip_cksum, udp_cksum) for idx, port, ip_cksum, udp_cksum in packets_info if udp_cksum != 0]
print(f"\nPaquets avec UDP checksum != 0: {len(non_zero_udp)}")
for item in non_zero_udp[:10]:
    print(f"  {item}")