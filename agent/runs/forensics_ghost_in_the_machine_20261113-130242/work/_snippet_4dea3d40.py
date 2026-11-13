import struct

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

# Chaque paquet commence à positions[i] où i est pair
# Structure du paquet (à partir de positions[i]):
# offset 0-5: deadbeef 0002
# offset 6-11: deadbeef 0001
# offset 12-13: 0800
# offset 14-15: 4500
# offset 16-17: 0020 (IP total length)
# offset 18-19: IP ID
# offset 20-21: flags+frag
# offset 22-23: TTL+protocol
# offset 24-25: IP checksum
# offset 26-29: src IP
# offset 30-33: dst IP
# offset 34-35: src port
# offset 36-37: dst port
# offset 38-39: UDP length
# offset 40-41: UDP checksum
# offset 42-45: payload ("PING" + ?)

# Collecter les checksums UDP et IP ID
udp_checksums = []
ip_ids = []
src_ports = []

for i in range(0, len(positions), 2):
    start = positions[i]
    if start + 42 >= len(data):
        break
    
    # IP ID à offset 18-19
    ip_id = struct.unpack('>H', data[start+18:start+20])[0]
    ip_ids.append(ip_id)
    
    # UDP checksum à offset 40-41
    udp_cksum = struct.unpack('>H', data[start+40:start+42])[0]
    udp_checksums.append(udp_cksum)
    
    # Source port à offset 34-35
    src_port = struct.unpack('>H', data[start+34:start+36])[0]
    src_ports.append(src_port)

print(f"Nombre de paquets: {len(udp_checksums)}")

# Trouver les checksums UDP non nuls
non_zero_udp = [(i, v) for i, v in enumerate(udp_checksums) if v != 0]
print(f"\nChecksums UDP non nuls: {len(non_zero_udp)}")
for idx, val in non_zero_udp[:20]:
    print(f"  Packet {idx}: UDP checksum = {val} (0x{val:04x})")

# Vérifier les IP IDs
unique_ip_ids = set(ip_ids)
print(f"\nIP IDs uniques: {unique_ip_ids}")

# Vérifier les ports source
unique_ports = set(src_ports)
print(f"\nPorts source uniques: {len(unique_ports)}")
if len(unique_ports) < 20:
    print(f"  Ports: {sorted(unique_ports)}")
else:
    # Afficher les ports les plus fréquents
    from collections import Counter
    port_counts = Counter(src_ports)
    print(f"  Ports les plus fréquents: {port_counts.most_common(10)}")