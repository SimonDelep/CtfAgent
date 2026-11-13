import struct

# Re-lire le pcap et extraire les ports source uniques dans l'ordre
with open('capture.pcap', 'rb') as f:
    f.read(24)  # Skip pcap header
    
    packets = []
    while True:
        ts_sec = f.read(4)
        if len(ts_sec) < 4:
            break
        ts_sec = struct.unpack('<I', ts_sec)[0]
        ts_usec = struct.unpack('<I', f.read(4))[0]
        incl_len = struct.unpack('<I', f.read(4))[0]
        orig_len = struct.unpack('<I', f.read(4))[0]
        
        data = f.read(incl_len)
        
        if len(data) >= 42:
            udp = data[34:42]
            udp_src_port = struct.unpack('>H', udp[0:2])[0]
            packets.append(udp_src_port)

# Compter les occurrences
from collections import Counter
port_counts = Counter(packets)

# Extraire les ports qui n'apparaissent qu'une seule fois, dans l'ordre
singletons_in_order = []
for p in packets:
    if port_counts[p] == 1:
        singletons_in_order.append(p)

print(f"Nombre de singletons: {len(singletons_in_order)}")
print(f"Singletons dans l'ordre: {singletons_in_order[:50]}")

# Peut-être que les singletons contiennent le message
# Essayons de convertir les ports en bytes
# Les ports sont des valeurs 16-bit, peut-être qu'on doit prendre le byte de poids faible ou fort
bytes_low = [p & 0xFF for p in singletons_in_order]
bytes_high = [(p >> 8) & 0xFF for p in singletons_in_order]

print(f"\nBytes bas (low byte): {bytes_low[:50]}")
print(f"Bytes haut (high byte): {bytes_high[:50]}")

# Essayons de convertir en ASCII
try:
    msg_low = bytes(bytes_low).decode('ascii', errors='replace')
    print(f"\nMessage (low byte): {msg_low}")
except:
    pass

try:
    msg_high = bytes(bytes_high).decode('ascii', errors='replace')
    print(f"Message (high byte): {msg_high}")
except:
    pass
