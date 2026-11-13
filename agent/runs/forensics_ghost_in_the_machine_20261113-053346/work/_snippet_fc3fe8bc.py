import struct

def parse_pcap_full(pcap_path):
    with open(pcap_path, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        if magic == 0xa1b2c3c4:
            endian = '<'
        else:
            return []
        
        f.read(20)  # header PCAP
        
        packets = []
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            
            if len(data) >= 14 + 20 + 8:
                eth = data[:14]
                eth_type = struct.unpack('>H', eth[12:14])[0]
                if eth_type == 0x0800:  # IPv4
                    ip = data[14:34]
                    src_ip = '.'.join(str(b) for b in ip[12:16])
                    dst_ip = '.'.join(str(b) for b in ip[16:20])
                    proto = ip[9]
                    if proto == 17:  # UDP
                        udp = data[34:42]
                        src_port = struct.unpack('>H', udp[0:2])[0]
                        dst_port = struct.unpack('>H', udp[2:4])[0]
                        payload = data[42:]
                        packets.append({
                            'src_ip': src_ip,
                            'dst_ip': dst_ip,
                            'src_port': src_port,
                            'dst_port': dst_port,
                            'payload': payload,
                            'ts': ts_sec + ts_usec / 1e6
                        })
    return packets

packets = parse_pcap_full('capture.pcap')
print(f"Total paquets: {len(packets)}")

# Regardons les ports de destination
dst_ports = [p['dst_port'] for p in packets]
from collections import Counter
dst_counts = Counter(dst_ports)
print(f"\nPorts de destination les plus fréquents:")
for port, cnt in dst_counts.most_common(10):
    print(f"  {port}: {cnt}")

# Regardons les IPs
src_ips = Counter(p['src_ip'] for p in packets)
dst_ips = Counter(p['dst_ip'] for p in packets)
print(f"\nIPs sources: {src_ips}")
print(f"IPs destinations: {dst_ips}")

# Regardons les payloads
payloads = Counter(p['payload'] for p in packets)
print(f"\nPayloads uniques: {len(payloads)}")
for payload, cnt in list(payloads.items())[:5]:
    print(f"  {payload!r}: {cnt}")
