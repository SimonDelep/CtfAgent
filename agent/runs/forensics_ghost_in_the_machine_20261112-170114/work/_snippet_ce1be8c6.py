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

# Extraire TTL
ttls = []
for i, p in enumerate(packets):
    payload = p['payload']
    if len(payload) >= 13:
        ttl = payload[12]  # TTL est à l'offset 12 du payload (byte 10 de l'IP header)
        ttls.append({'idx': i, 'ts_usec': p['ts_usec'], 'ttl': ttl})

# Compter les TTL
ttl_counts = Counter(v['ttl'] for v in ttls)
print("Distribution TTL:", dict(ttl_counts))

# Convertir en bits (152 et 201)
# 152 = 0x98, 201 = 0xC9
# Peut-être que c'est un bit de signal ?
# 152 vs 201 - la différence est 49

# Regardons la séquence de TTL
ttl_sequence = [v['ttl'] for v in ttls]
print(f"\nPremiers 20 TTLs: {ttl_sequence[:20]}")

# Convertir en binaire (0 pour 152, 1 pour 201)
bit_sequence = [0 if t == 152 else 1 if t == 201 else -1 for t in ttl_sequence]
print(f"Premiers 20 bits: {bit_sequence[:20]}")

# Regardons si on peut lire quelque chose en groupes de 8
bits_only = [b for b in bit_sequence if b != -1]
print(f"Nombre de bits valides: {len(bits_only)}")

# Essayer de convertir en bytes
if len(bits_only) >= 8:
    bytes_result = []
    for i in range(0, len(bits_only) - 7, 8):
        byte_bits = bits_only[i:i+8]
        byte_val = 0
        for j, b in enumerate(byte_bits):
            byte_val |= (b << (7-j))
        bytes_result.append(byte_val)
    print(f"Bytes décodés (premiers 20): {bytes_result[:20]}")
    print(f"En ASCII: {bytes(bytes_result[:20])}")
