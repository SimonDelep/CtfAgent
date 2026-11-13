import struct
from collections import Counter

# Lire le pcap
with open('capture.pcap', 'rb') as f:
    magic = f.read(4)
    f.read(20)  # skip rest of header
    
    packets = []
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) >= 42:
            src_port = struct.unpack('>H', pkt_data[34:36])[0]
            packets.append(src_port)

counts = Counter(packets)
singletons = [port for port, count in counts.items() if count == 1]
frequent = [port for port, count in counts.items() if count >= 60]

# Singleton ports in order of appearance
singleton_order = []
seen = set()
for port in packets:
    if counts[port] == 1 and port not in seen:
        singleton_order.append(port)
        seen.add(port)

# Get singleton values mod 256
singleton_mod256 = [p % 256 for p in singleton_order]
print("Singleton mod 256 (first 30):", singleton_mod256[:30])

# Maybe the key is derived from frequent ports?
# Let's see frequent ports mod 256
frequent_mod256 = [p % 256 for p in frequent]
print("Frequent ports mod 256:", frequent_mod256)

# Try XORing singleton mod 256 with frequent ports mod 256 (repeating key)
key = frequent_mod256
key_extended = (key * (len(singleton_mod256) // len(key) + 1))[:len(singleton_mod256)]
xored = [s ^ k for s, k in zip(singleton_mod256, key_extended)]
print("XOR result (first 30):", xored[:30])
print("XOR as chars:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in xored[:50]))

# Maybe the key is just the frequent ports in order, repeated?
# Or maybe we need to use a different approach
# Let's try: what if the message is in the singleton ports directly?
# And the key is something else?

# Try interpreting singleton mod 256 as ASCII
print("\nSingleton mod 256 as ASCII:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in singleton_mod256[:50]))