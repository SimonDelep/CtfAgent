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

# Regardons les payloads
payloads = [p['payload'] for p in packets]

# Combien de payloads uniques ?
unique_payloads = set(payloads)
print(f"Nombre de payloads uniques: {len(unique_payloads)}")

# Affichons quelques payloads différents
for i, p in enumerate(payloads[:10]):
    print(f"Payload {i}: {p.hex()} -> {p}")

# Cherchons les variations
# Peut-être que le payload contient des données différentes
# Regardons les différences entre les payloads

# D'abord, voyons si tous les payloads sont identiques
first_payload = payloads[0]
different_count = sum(1 for p in payloads if p != first_payload)
print(f"\nPayloads différents du premier: {different_count}")

# Si tous sont identiques, cherchons ailleurs
# Peut-être dans les timestamps ou dans d'autres champs
