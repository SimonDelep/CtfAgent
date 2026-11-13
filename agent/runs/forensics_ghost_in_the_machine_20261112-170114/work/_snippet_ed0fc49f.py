import struct

with open('capture.pcap', 'rb') as f:
    global_header = f.read(24)
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        # La structure semble être:
        # deadbeef (4) + X (2) + deadbeef (4) + Y (2) + payload
        # Mais incl_len=46, donc 46 bytes de données
        
        # Analysons la structure
        if len(pkt_data) >= 12:
            marker1 = pkt_data[0:4]
            val1 = struct.unpack('>H', pkt_data[4:6])[0]
            marker2 = pkt_data[6:10]
            val2 = struct.unpack('>H', pkt_data[10:12])[0]
            payload = pkt_data[12:]
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'val1': val1,
                'val2': val2,
                'payload': payload
            })

print(f"Total packets: {len(packets)}")

# Regardons les valeurs uniques
val1_set = set(p['val1'] for p in packets)
val2_set = set(p['val2'] for p in packets)
print(f"\nval1 unique values: {sorted(val1_set)}")
print(f"val2 unique values: {sorted(val2_set)}")

# Compter les occurrences
from collections import Counter
val1_counts = Counter(p['val1'] for p in packets)
val2_counts = Counter(p['val2'] for p in packets)
print(f"\nval1 counts: {dict(val1_counts)}")
print(f"val2 counts: {dict(val2_counts)}")
