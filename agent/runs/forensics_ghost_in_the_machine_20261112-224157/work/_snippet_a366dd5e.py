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
        timestamps.append(ts_usec)

print(f"Total packets: {len(src_ports)}")
print(f"Unique src_ports: {len(set(src_ports))}")

# Show some port values
print("\nFirst 30 src_ports:")
for i, p in enumerate(src_ports[:30]):
    print(f"  {i}: {p}")

# Check if ports are in a certain range
print(f"\nMin port: {min(src_ports)}")
print(f"Max port: {max(src_ports)}")

# Look for patterns - maybe ports encode something
# Check if ports are even/odd or have some property
even_count = sum(1 for p in src_ports if p % 2 == 0)
odd_count = len(src_ports) - even_count
print(f"\nEven ports: {even_count}, Odd ports: {odd_count}")

# Maybe the ports encode bytes? Let's see if they're in 0-255 range
ports_in_range = [p for p in src_ports if p < 256]
print(f"Ports < 256: {len(ports_in_range)}")

# Or maybe we need to look at the difference between consecutive ports
diffs = [src_ports[i+1] - src_ports[i] for i in range(len(src_ports)-1)]
print(f"\nUnique diffs: {len(set(diffs))}")
print(f"Min diff: {min(diffs)}, Max diff: {max(diffs)}")