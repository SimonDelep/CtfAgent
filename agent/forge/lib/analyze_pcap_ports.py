SCHEMA = {
  "name": "analyze_pcap_ports",
  "description": "Analyse les ports sources et leurs fréquences dans le PCAP, identifie les singletons et les ports fréquents",
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
from collections import Counter

def main(args):
    def parse_pcap(pcap_file):
        packets = []
        with open(pcap_file, 'rb') as f:
            # Skip global header (24 bytes)
            f.read(24)
            
            while True:
                # Read packet header (16 bytes)
                pkt_hdr = f.read(16)
                if len(pkt_hdr) < 16:
                    break
                
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_hdr)
                data = f.read(incl_len)
                
                if len(data) < 28:  # Ethernet(14) + IP(20) + UDP(8) minimum
                    continue
                
                # Parse Ethernet header (14 bytes)
                eth_dst = data[0:6]
                eth_src = data[6:12]
                eth_type = struct.unpack('>H', data[12:14])[0]
                
                if eth_type != 0x0800:  # Not IPv4
                    continue
                
                # IP header starts at byte 14
                ip_header = data[14:34]
                ip_proto = ip_header[9]
                
                if ip_proto != 17:  # Not UDP
                    continue
                
                # UDP header starts at byte 34
                udp_header = data[34:42]
                src_port, dst_port, udp_len, checksum = struct.unpack('>HHHH', udp_header)
                
                # UDP data starts at byte 42
                udp_data = data[42:42+udp_len-8]
                
                packets.append({
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'udp_len': udp_len,
                    'data': udp_data
                })
        
        return packets

    packets = parse_pcap(args['pcap_file'])

    # Count port frequencies
    src_port_counts = Counter(p['src_port'] for p in packets)

    # Find singletons (ports appearing exactly once)
    singletons = [p for p in packets if src_port_counts[p['src_port']] == 1]
    singleton_ports = [p['src_port'] for p in singletons]

    # Find frequent ports (appearing many times)
    frequent_ports = [(port, count) for port, count in src_port_counts.items() if count > 1]
    frequent_ports_sorted = sorted(frequent_ports, key=lambda x: -x[1])

    print(f"Total packets: {len(packets)}")
    print(f"Unique src_ports: {len(src_port_counts)}")
    print(f"Singletons: {len(singletons)}")
    print(f"Singleton ports: {singleton_ports[:20]}...")
    print(f"\nTop frequent ports:")
    for port, count in frequent_ports_sorted[:15]:
        print(f"  Port {port}: {count} occurrences")

    # Show first few singletons with their packet index
    print(f"\nFirst 10 singletons (packet_index, src_port):")
    count = 0
    for i, p in enumerate(packets):
        if src_port_counts[p['src_port']] == 1:
            print(f"  Pkt {i}: src_port={p['src_port']}")
            count += 1
            if count >= 10:
                break

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
