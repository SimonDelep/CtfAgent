import struct

# Re-lire le pcap
with open('capture.pcap', 'rb') as f:
    f.read(24)
    
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

from collections import Counter
port_counts = Counter(packets)

# Les ports fréquents (plus de 1 occurrence)
frequent_ports = [p for p, c in port_counts.items() if c > 1]
print(f"Ports fréquents: {sorted(frequent_ports)}")

# Regardons les bytes de ces ports
for port in sorted(frequent_ports):
    low = port & 0xFF
    high = (port >> 8) & 0xFF
    print(f"Port {port}: high={high}, low={low}, as_char_low={chr(low) if 32 <= low < 127 else '?'}")

# Peut-être que les ports fréquents forment un mot en ASCII
# Regardons les low bytes des ports fréquents
low_bytes_frequent = sorted([p & 0xFF for p in frequent_ports])
print(f"\nLow bytes des ports fréquents (triés): {low_bytes_frequent}")

# Essayons de voir si c'est un mot
try:
    msg = bytes(low_bytes_frequent).decode('ascii', errors='replace')
    print(f"Message possible: {msg}")
except:
    pass
