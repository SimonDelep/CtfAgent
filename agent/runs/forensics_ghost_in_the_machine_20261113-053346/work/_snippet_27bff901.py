import struct
from collections import Counter

# Lire le pcap
with open('capture.pcap', 'rb') as f:
    magic = f.read(4)
    f.read(20)
    
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

# Singleton ports in order of appearance
singleton_order = []
seen = set()
for port in packets:
    if counts[port] == 1 and port not in seen:
        singleton_order.append(port)
        seen.add(port)

# Get singleton values mod 256
singleton_mod256 = [p % 256 for p in singleton_order]

# If message starts with "csaw{", what would the key be?
expected_start = "csaw{"
key_from_start = [singleton_mod256[i] ^ ord(expected_start[i]) for i in range(len(expected_start))]
print("Key derived from 'csaw{':", key_from_start)
print("Key as chars:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in key_from_start))

# Maybe the key is related to the frequent ports?
frequent = [port for port, count in counts.items() if count >= 60]
frequent_sorted = sorted(frequent)
print("\nFrequent ports sorted:", frequent_sorted)
print("Frequent ports mod 256:", [p % 256 for p in frequent_sorted])

# What if the key is the frequent ports mod 256, but we need to find the right order?
# Or maybe the key is derived from the frequent ports in some other way?

# Let's try: what if we XOR all singletons with a repeating key derived from frequent ports?
# First, let's see if there's a pattern in the frequent ports
print("\nFrequent ports:", frequent)
for p in frequent:
    print(f"  {p} = {bin(p)} = mod256={p%256}")