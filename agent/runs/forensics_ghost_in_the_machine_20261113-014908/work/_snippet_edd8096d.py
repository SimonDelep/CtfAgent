import struct
from collections import Counter

# Re-lire le pcap et analyser chaque paquet
with open('capture.pcap', 'rb') as f:
    f.read(24)
    
    packets = []
    
    while True:
        pkt_hdr = f.read(16)
        if len(pkt_hdr) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_hdr)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 42:
            udp_start = 34
            src_port = struct.unpack('>H', pkt_data[udp_start:udp_start+2])[0]
            dst_port = struct.unpack('>H', pkt_data[udp_start+2:udp_start+4])[0]
            packets.append((src_port, dst_port))

# Analyser la structure : pour chaque paquet, quel port est "unique" et quel port est "fréquent"
all_ports = [p for pair in packets for p in pair]
port_counts = Counter(all_ports)

# Pour chaque paquet, identifier si c'est un "signal" (contient un singleton) ou un "leurre"
signal_packets = []
leather_packets = []

for i, (src, dst) in enumerate(packets):
    src_is_singleton = port_counts[src] == 1
    dst_is_singleton = port_counts[dst] == 1
    
    if src_is_singleton or dst_is_singleton:
        signal_packets.append((i, src, dst))
    else:
        leather_packets.append((i, src, dst))

print(f"Paquets signal: {len(signal_packets)}")
print(f"Paquets leurre: {len(leather_packets)}")

# Les paquets signal contiennent les singletons
# Regardons les premiers paquets signal
print("\nPremiers paquets signal (index, src, dst):")
for i, src, dst in signal_packets[:20]:
    print(f"  {i}: src={src} ({port_counts[src]}), dst={dst} ({port_counts[dst]})")
