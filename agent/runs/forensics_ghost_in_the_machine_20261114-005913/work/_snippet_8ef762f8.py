# Analyser les ports fréquents pour trouver la clé
with open('capture.pcap', 'rb') as f:
    data = f.read()

deadbeef = b'\xde\xad\xbe\xef'
positions = []
pos = 0
while True:
    pos = data.find(deadbeef, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

packets = []
for i in range(0, len(positions), 2):
    start = positions[i]
    ip_start = start + 14
    
    if ip_start + 28 > len(data):
        continue
    
    ip_header = data[ip_start:ip_start+20]
    ip_ihl = (ip_header[0] & 0xF) * 4
    src_ip = '.'.join(str(b) for b in ip_header[12:16])
    dst_ip = '.'.join(str(b) for b in ip_header[16:20])
    
    udp_start = ip_start + ip_ihl
    if udp_start + 8 > len(data):
        continue
    
    udp_header = data[udp_start:udp_start+8]
    src_port = int.from_bytes(udp_header[0:2], 'big')
    dst_port = int.from_bytes(udp_header[2:4], 'big')
    udp_len = int.from_bytes(udp_header[4:6], 'big')
    
    payload_start = udp_start + 8
    payload_len = udp_len - 8
    payload = data[payload_start:payload_start+payload_len]
    
    packets.append({
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'src_port': src_port,
        'dst_port': dst_port,
        'payload': payload,
        'offset': start
    })

from collections import Counter
src_ports = [p['src_port'] for p in packets]
port_counts = Counter(src_ports)

# Ports fréquents (plus de 1 occurrence)
frequent_ports = [port for port, count in port_counts.items() if count > 1]
print(f"Ports fréquents: {len(frequent_ports)}")
print(f"Ports fréquents: {sorted(frequent_ports)}")

# Essayer de dériver une clé à partir des ports fréquents
# Peut-être modulo 256 pour obtenir des caractères ASCII
key_bytes = [port % 256 for port in sorted(frequent_ports)]
print(f"\nBytes dérivés (port % 256): {key_bytes[:20]}")

# Essayer de convertir en string
try:
    key_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in key_bytes)
    print(f"Clé potentielle: {key_str}")
except:
    pass

# Regardons aussi les valeurs modulo 256 des ports singletons
singleton_ports = [port for port, count in port_counts.items() if count == 1]
singleton_ports_sorted = sorted(singleton_ports)
print(f"\nPorts singletons triés: {singleton_ports_sorted[:20]}")
print(f"Singletons % 256: {[p % 256 for p in singleton_ports_sorted[:20]]}")