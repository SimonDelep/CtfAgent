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
        
        # Structure: deadbeef (4) + X (2) + deadbeef (4) + Y (2) + Ethernet/IP/UDP
        # Ethernet/IP commence à offset 12
        if len(pkt_data) >= 12:
            val1 = struct.unpack('>H', pkt_data[4:6])[0]
            val2 = struct.unpack('>H', pkt_data[10:12])[0]
            
            # Header IP commence à offset 12
            ip_header = pkt_data[12:32]  # 20 bytes
            
            # TTL est à l'offset 10 du header IP (offset 22 du paquet)
            ttl = pkt_data[22]
            
            # Protocol est à l'offset 9 du header IP (offset 21 du paquet)
            protocol = pkt_data[21]
            
            # Source IP
            src_ip = pkt_data[26:30]
            
            # Dest IP
            dst_ip = pkt_data[30:34]
            
            # Après header IP (32 bytes), c'est le header UDP
            # Header UDP: src_port (2) + dst_port (2) + length (2) + checksum (2) + data
            if len(pkt_data) >= 40:
                udp_start = 32
                src_port = struct.unpack('>H', pkt_data[udp_start:udp_start+2])[0]
                dst_port = struct.unpack('>H', pkt_data[udp_start+2:udp_start+4])[0]
                udp_length = struct.unpack('>H', pkt_data[udp_start+4:udp_start+6])[0]
                udp_checksum = struct.unpack('>H', pkt_data[udp_start+6:udp_start+8])[0]
                udp_data = pkt_data[udp_start+8:]
            else:
                src_port = dst_port = udp_length = udp_checksum = 0
                udp_data = b''
            
            packets.append({
                'ts_sec': ts_sec,
                'ts_usec': ts_usec,
                'val1': val1,
                'val2': val2,
                'ttl': ttl,
                'protocol': protocol,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'udp_data': udp_data
            })

print(f"Total packets: {len(packets)}")

# Regardons les ports sources
src_ports = Counter(p['src_port'] for p in packets)
print(f"\nPorts sources: {dict(src_ports)}")

# Regardons les ports destinations
dst_ports = Counter(p['dst_port'] for p in packets)
print(f"Ports destinations: {dict(dst_ports)}")

# Regardons les TTLs
ttls = Counter(p['ttl'] for p in packets)
print(f"TTLs: {dict(ttls)}")
