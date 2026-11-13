# Clé potentielle : les 6 ports principaux dans l'ordre d'apparition
key_ports = [40115, 40104, 40052, 40100, 40111, 40119]
key_bytes = [p % 256 for p in key_ports]
print(f"Clé potentielle (mod 256): {key_bytes}")

# Extraire les singletons
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

print(f"Nombre de singletons: {len(singletons)}")

# XOR avec la clé répétée
key_len = len(key_bytes)
decrypted = []
for i, s in enumerate(singletons):
    key_byte = key_bytes[i % key_len]
    decrypted_byte = (s % 256) ^ key_byte
    decrypted.append(decrypted_byte)

print(f"Decrypté (premiers 50 bytes): {decrypted[:50]}")
print(f"Decrypté en ASCII: {bytes(decrypted[:50])}")

# Essayer de voir si c'est lisible
try:
    text = bytes(decrypted).decode('ascii', errors='replace')
    print(f"Texte ASCII: {text[:100]}")
except:
    pass
