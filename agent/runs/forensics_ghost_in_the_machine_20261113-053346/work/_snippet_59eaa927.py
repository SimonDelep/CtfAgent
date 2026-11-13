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

# Maybe the message is the XOR of consecutive singletons?
# Or maybe we need to look at the difference between consecutive singletons?
diffs = [singleton_mod256[i+1] - singleton_mod256[i] for i in range(len(singleton_mod256)-1)]
print("Differences (first 30):", diffs[:30])

# Maybe the key is embedded in the frequent ports in a different way?
# Let's look at the frequent ports more carefully
frequent = [port for port, count in counts.items() if count >= 60]
frequent_in_order = []
seen = set()
for port in packets:
    if port in frequent and port not in seen:
        frequent_in_order.append(port)
        seen.add(port)

print("\nFrequent ports in order of first appearance:", frequent_in_order)

# What if the key is the XOR of all frequent ports?
xor_all_frequent = 0
for p in frequent:
    xor_all_frequent ^= (p % 256)
print("XOR of all frequent ports mod 256:", xor_all_frequent)

# What if we need to use the frequent ports as a key in a different way?
# Let's try: maybe the message is XORed with a key that's derived from the frequent ports
# in order of appearance, repeated?

key = [p % 256 for p in frequent_in_order]
print("Key (frequent ports mod 256 in order):", key)

# Try XORing singleton_mod256 with this key (repeated)
key_extended = (key * (len(singleton_mod256) // len(key) + 1))[:len(singleton_mod256)]
xored = [s ^ k for s, k in zip(singleton_mod256, key_extended)]
print("XOR result (first 50):", xored[:50])
print("XOR as text:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in xored[:100]))