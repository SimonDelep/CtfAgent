import struct
from collections import defaultdict

# Re-lisons le pcap
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
    
    packets.append(pkt_data)

# Collectons les ports source pour TTL=64 (bruit) et TTL=113 (signal)
noise_ports = []  # TTL=64
signal_ports = []  # TTL=113

for i, pkt in enumerate(packets):
    ttl = pkt[22]
    udp_start = 34
    src_port = struct.unpack('>H', pkt[udp_start:udp_start+2])[0]
    
    if ttl == 64:
        noise_ports.append((i, src_port))
    elif ttl == 113:
        signal_ports.append((i, src_port))

print(f"Nombre de ports bruit (TTL=64): {len(noise_ports)}")
print(f"Nombre de ports signal (TTL=113): {len(signal_ports)}")

# Regardons les ports bruit - ils devraient tous être dans la plage 40000-40199
noise_port_values = [p[1] for p in noise_ports]
print(f"\nPort bruit min: {min(noise_port_values)}, max: {max(noise_port_values)}")

# Regardons les ports signal
signal_port_values = [p[1] for p in signal_ports]
print(f"Port signal min: {min(signal_port_values)}, max: {max(signal_port_values)}")

# Peut-être que le port source contient l'information
# Essayons de voir si les ports bruit ont une structure particulière
print("\nAnalyse des ports bruit:")
from collections import Counter
noise_counts = Counter(noise_port_values)
print(f"Ports bruit uniques: {len(noise_counts)}")
for port, count in sorted(noise_counts.items())[:10]:
    print(f"  Port {port}: {count} fois")