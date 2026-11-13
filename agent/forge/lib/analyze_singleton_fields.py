SCHEMA = {
  "name": "analyze_singleton_fields",
  "description": "Extrait tous les champs des paquets UDP singletons (port, checksum, TTL, payload) et les affiche pour analyse",
  "parameters": {
    "properties": {
      "pcap_file": {
        "description": "Chemin du fichier pcap",
        "type": "string"
      }
    },
    "type": "object"
  }
}

import struct
from collections import defaultdict

def main(args):
    pcap_file = args.get('pcap_file', 'capture.pcap')
    
    with open(pcap_file, 'rb') as f:
        # Skip pcap global header (24 bytes)
        f.read(24)
        
        packets = []
        while True:
            # Read packet header (16 bytes)
            pkt_header = f.read(16)
            if len(pkt_header) < 16:
                break
            
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_header)
            pkt_data = f.read(incl_len)
            
            # Parse Ethernet (14 bytes) + IP (20 bytes min) + UDP (8 bytes)
            if len(pkt_data) < 42:  # Ethernet(14) + IP(20) + UDP(8)
                continue
            
            # IP header
            ip_start = 14
            ip_header = pkt_data[ip_start:ip_start+20]
            ip_version_ihl = ip_header[0]
            ip_ihl = (ip_version_ihl & 0x0F) * 4
            ip_ttl = ip_header[8]
            ip_proto = ip_header[9]
            ip_checksum = struct.unpack('!H', ip_header[10:12])[0]
            ip_src = '.'.join(str(b) for b in ip_header[12:16])
            ip_dst = '.'.join(str(b) for b in ip_header[16:20])
            
            # UDP header
            udp_start = ip_start + ip_ihl
            if len(pkt_data) < udp_start + 8:
                continue
            udp_header = pkt_data[udp_start:udp_start+8]
            src_port, dst_port, udp_len, udp_checksum = struct.unpack('!HHHH', udp_header)
            
            # UDP payload
            payload = pkt_data[udp_start+8:]
            
            packets.append({
                'ts': ts_sec * 1000000 + ts_usec,
                'src_port': src_port,
                'dst_port': dst_port,
                'ip_ttl': ip_ttl,
                'ip_checksum': ip_checksum,
                'udp_checksum': udp_checksum,
                'payload': payload,
                'ip_src': ip_src,
                'ip_dst': ip_dst
            })
    
    # Count port frequencies
    port_counts = defaultdict(int)
    for p in packets:
        port_counts[p['src_port']] += 1
    
    # Find singletons (ports appearing exactly once)
    singleton_ports = {port for port, count in port_counts.items() if count == 1}
    
    # Get singleton packets in timestamp order
    singleton_packets = [p for p in packets if p['src_port'] in singleton_ports]
    singleton_packets.sort(key=lambda x: x['ts'])
    
    print(f"Total packets: {len(packets)}")
    print(f"Singleton ports: {len(singleton_ports)}")
    print(f"Singleton packets in order: {len(singleton_packets)}")
    print()
    
    # Show first 20 singleton packets with all fields
    print("First 20 singleton packets:")
    print("=" * 100)
    for i, p in enumerate(singleton_packets[:20]):
        payload_str = p['payload'][:20] if p['payload'] else b''
        print(f"{i:3d}: port={p['src_port']:5d} ttl={p['ip_ttl']:3d} ip_chk={p['ip_checksum']:5d} udp_chk={p['udp_checksum']:5d} payload={payload_str}")
    
    print()
    print("All singleton ports (in timestamp order):")
    print([p['src_port'] for p in singleton_packets])
    
    # Try XOR with sh4dow on different fields
    key = b'sh4dow'
    print()
    print("XOR attempts on src_port % 256:")
    result = ''.join(chr((p['src_port'] % 256) ^ key[i % len(key)]) for i, p in enumerate(singleton_packets))
    print(result[:50])
    
    print()
    print("XOR attempts on ip_ttl:")
    result = ''.join(chr(p['ip_ttl'] ^ key[i % len(key)]) for i, p in enumerate(singleton_packets))
    print(result[:50])
    
    print()
    print("XOR attempts on ip_checksum (low byte):")
    result = ''.join(chr((p['ip_checksum'] & 0xFF) ^ key[i % len(key)]) for i, p in enumerate(singleton_packets))
    print(result[:50])
    
    print()
    print("XOR attempts on udp_checksum (low byte):")
    result = ''.join(chr((p['udp_checksum'] & 0xFF) ^ key[i % len(key)]) for i, p in enumerate(singleton_packets))
    print(result[:50])
    
    return singleton_packets

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
