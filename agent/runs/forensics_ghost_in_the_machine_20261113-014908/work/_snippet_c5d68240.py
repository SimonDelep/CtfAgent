# Ports principaux (64-65 occurrences)
main_frequent = [40052, 40100, 40104, 40111, 40115, 40119]

print("Ports principaux mod 256:")
for p in main_frequent:
    print(f"  {p} -> {p % 256} -> {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")

# Peut-être que la clé est la séquence de ces ports dans un ordre spécifique
# Ou peut-être que chaque singleton est XORé avec un port fréquent correspondant

# Regardons les singletons et essayons de trouver un pattern
# Si le flag commence par "csaw{", alors les premiers singletons XOR clé devraient donner "csaw{"

# Extraire les singletons dans l'ordre
import struct
from collections import Counter

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

all_ports = [p for pair in packets for p in pair]
port_counts = Counter(all_ports)

# Extraire les singletons dans l'ordre d'apparition
singletons = []
seen = set()
for src, dst in packets:
    if port_counts[src] == 1 and src not in seen:
        singletons.append(src)
        seen.add(src)

print(f"\nNombre de singletons: {len(singletons)}")
print(f"Premiers 20 singletons: {singletons[:20]}")
print(f"Singletons mod 256: {[s % 256 for s in singletons[:20]]}")

# Si on suppose que le flag commence par "csaw{", essayons de trouver la clé
# singleton[i] XOR key[i] = ord('csaw{'[i])
target = b'csaw{'
print(f"\nSi le flag commence par 'csaw{{':")
for i in range(5):
    s = singletons[i] % 256
    expected = target[i]
    key_byte = s ^ expected
    print(f"  singleton[{i}]={s} XOR key={key_byte} = {chr(key_byte)} (target '{chr(expected)}')")
