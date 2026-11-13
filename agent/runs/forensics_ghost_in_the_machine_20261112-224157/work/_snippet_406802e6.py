import struct

with open('capture_fixed.pcap', 'rb') as f:
    f.read(24)  # Skip global header
    
    src_ports = []
    timestamps = []
    
    while True:
        pkt_header = f.read(16)
        if len(pkt_header) < 16:
            break
        
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_header)
        pkt_data = f.read(incl_len)
        
        if len(pkt_data) < 42:
            continue
        
        # IP header
        ip_start = 14
        ip_header = pkt_data[ip_start:ip_start+20]
        ip_header_len = (ip_header[0] & 0x0F) * 4
        
        # UDP header
        udp_start = ip_start + ip_header_len
        udp_header = pkt_data[udp_start:udp_start+8]
        src_port = struct.unpack('>H', udp_header[0:2])[0]
        
        src_ports.append(src_port)
        timestamps.append((ts_sec, ts_usec))

# Look at time differences between packets
time_diffs = []
for i in range(len(timestamps)-1):
    t1_sec, t1_usec = timestamps[i]
    t2_sec, t2_usec = timestamps[i+1]
    diff_us = (t2_sec - t1_sec) * 1000000 + (t2_usec - t1_usec)
    time_diffs.append(diff_us)

print(f"Time diffs (us):")
print(f"  Min: {min(time_diffs)}")
print(f"  Max: {max(time_diffs)}")
print(f"  Unique values: {len(set(time_diffs))}")

# Show unique time diffs
unique_diffs = sorted(set(time_diffs))
print(f"\nUnique time diffs: {unique_diffs[:20]}...")

# Maybe the time diffs encode something
# Check if they're multiples of some value
print(f"\nGCD of time diffs?")
import math
g = time_diffs[0]
for d in time_diffs[1:]:
    g = math.gcd(g, d)
print(f"GCD: {g}")

# Check if time diffs are multiples of 50000 (50ms) or similar
for base in [1000, 5000, 10000, 50000, 100000]:
    multiples = [d for d in time_diffs if d % base == 0]
    print(f"Multiples of {base}: {len(multiples)}/{len(time_diffs)}")