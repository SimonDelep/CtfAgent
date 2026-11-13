import struct
from collections import Counter

with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 12:
            val1 = struct.unpack('>H', pkt_data[4:6])[0]
            val2 = struct.unpack('>H', pkt_data[10:12])[0]
            
            ttl = pkt_data[22]
            
            if len(pkt_data) >= 40:
                udp_start = 32
                src_port = struct.unpack('>H', pkt_data[udp_start:udp_start+2])[0]
                dst_port = struct.unpack('>H', pkt_data[udp_start+2:udp_start+4])[0]
                udp_data = pkt_data[udp_start+8:]
            else:
                src_port = dst_port = 0
                udp_data = b''
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'ttl': ttl,
                'src_port': src_port,
                'dst_port': dst_port,
                'udp_data': udp_data
            })

# Trier par timestamp
packets.sort(key=lambda p: (p['ts_sec'], p['ts_usec']))

# Ports fréquents (la clé potentielle)
frequent_ports = [40052, 40100, 40104, 40111, 40115, 40119]
frequent_set = set(frequent_ports)

# Séparer les paquets en "clé" et "données"
key_packets = [p for p in packets if p['dst_port'] in frequent_set]
data_packets = [p for p in packets if p['dst_port'] not in frequent_set]

print(f"Paquets de clé: {len(key_packets)}")
print(f"Paquets de données: {len(data_packets)}")

# Les paquets de données ont des ports uniques - peut-être que le port lui-même encode un byte
# Regardons les ports de données
data_ports = [p['dst_port'] for p in data_packets]
print(f"\nPorts de données (premiers 20): {data_ports[:20]}")

# Peut-être que le port de destination modulo 256 donne un byte
data_bytes = [p % 256 for p in data_ports]
print(f"Ports mod 256 (premiers 20): {data_bytes[:20]}")

# Ou peut-être que c'est (port - offset) / quelque chose
# Regardons la distribution des ports de données
from collections import Counter
data_port_counts = Counter(data_ports)
print(f"\nComptage des ports de données: {dict(data_port_counts)}")
