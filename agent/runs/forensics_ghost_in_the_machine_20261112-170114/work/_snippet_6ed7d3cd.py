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
            payload = pkt_data[12:]
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'val1': val1,
                'val2': val2,
                'payload': payload
            })

# Le payload est: 0800 (Ethernet) + IP header (20 bytes) + ICMP
# IP header: bytes 2-21 du payload
# ICMP commence à byte 22 du payload

# Structure ICMP:
# Type (1 byte) + Code (1 byte) + Checksum (2 bytes) + Rest (variable)
# Pour PING (Echo Request): Type=8, Code=0

# Regardons les données ICMP
icmp_data = []
for i, p in enumerate(packets):
    payload = p['payload']
    if len(payload) >= 26:  # 2 + 20 + 4 (minimum ICMP)
        icmp_start = 22  # Après Ethernet (2) + IP (20)
        icmp_type = payload[icmp_start]
        icmp_code = payload[icmp_start + 1]
        icmp_checksum = struct.unpack('>H', payload[icmp_start + 2:icmp_start + 4])[0]
        icmp_data_part = payload[icmp_start + 4:]  # Données ICMP
        
        icmp_data.append({
            'idx': i,
            'ts_usec': p['ts_usec'],
            'icmp_type': icmp_type,
            'icmp_code': icmp_code,
            'icmp_checksum': icmp_checksum,
            'icmp_data': icmp_data_part
        })

# Vérifier les types ICMP
type_counts = Counter(d['icmp_type'] for d in icmp_data)
code_counts = Counter(d['icmp_code'] for d in icmp_data)
checksum_counts = Counter(d['icmp_checksum'] for d in icmp_data)

print("Types ICMP:", dict(type_counts))
print("Codes ICMP:", dict(code_counts))
print("Checksums ICMP uniques:", len(checksum_counts))

# Regardons les données ICMP
# Le payload ICMP devrait contenir "PING" + quelque chose
# Regardons les premières données ICMP
for i in range(5):
    print(f"ICMP data {i}: {icmp_data[i]['icmp_data'].hex()} -> {icmp_data[i]['icmp_data']}")
