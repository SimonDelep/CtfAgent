SCHEMA = {
  "name": "extract_signal_and_key",
  "description": "Extrait les ports singletons (signal) et les ports fréquents dans l'ordre d'apparition",
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
from collections import Counter, OrderedDict

def main(args):
    def parse_pcap(pcap_file):
        packets = []
        with open(pcap_file, 'rb') as f:
            f.read(24)  # Skip global header
            
            while True:
                pkt_hdr = f.read(16)
                if len(pkt_hdr) < 16:
                    break
                
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_hdr)
                data = f.read(incl_len)
                
                if len(data) < 42:
                    continue
                
                eth_type = struct.unpack('>H', data[12:14])[0]
                if eth_type != 0x0800:
                    continue
                
                ip_proto = data[23]
                if ip_proto != 17:
                    continue
                
                udp_header = data[34:42]
                src_port, dst_port, udp_len, checksum = struct.unpack('>HHHH', udp_header)
                udp_data = data[42:42+udp_len-8]
                
                packets.append({
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'udp_len': udp_len,
                    'data': udp_data
                })
        
        return packets

    packets = parse_pcap(args['pcap_file'])
    src_port_counts = Counter(p['src_port'] for p in packets)

    # Extract singleton ports in order of appearance
    singleton_ports = [p['src_port'] for p in packets if src_port_counts[p['src_port']] == 1]
    
    # Find the 6 main frequent ports (those with ~64 occurrences)
    frequent_port_counts = [(port, count) for port, count in src_port_counts.items() if count >= 60]
    frequent_ports = [port for port, count in sorted(frequent_port_counts, key=lambda x: -x[1])]
    
    print(f"Singleton ports count: {len(singleton_ports)}")
    print(f"Singleton ports (first 20): {singleton_ports[:20]}")
    print(f"\nFrequent ports (>=60 occurrences): {frequent_ports}")
    print(f"Counts: {[(p, src_port_counts[p]) for p in frequent_ports]}")
    
    # Extract the order of first appearance of each frequent port
    first_appearance = {}
    for i, p in enumerate(packets):
        if p['src_port'] in frequent_ports and p['src_port'] not in first_appearance:
            first_appearance[p['src_port']] = i
    
    print(f"\nFirst appearance of frequent ports:")
    for port in sorted(frequent_ports):
        print(f"  Port {port}: first seen at packet {first_appearance.get(port, 'N/A')}")
    
    # Order frequent ports by first appearance
    ordered_frequent = sorted(frequent_ports, key=lambda p: first_appearance.get(p, 999999))
    print(f"\nFrequent ports ordered by first appearance: {ordered_frequent}")
    
    # Try to create a key from these ports
    # Maybe the key is the ports repeated to match 112 bytes
    print(f"\nTrying XOR with singleton ports mod 256:")
    key_candidate = []
    for port in ordered_frequent:
        key_candidate.append(port % 256)
    
    # Repeat key to match 112 bytes
    key_extended = (key_candidate * (112 // len(key_candidate) + 1))[:112]
    
    print(f"Key candidate (mod 256): {key_candidate}")
    print(f"Extended key length: {len(key_extended)}")
    
    # XOR
    result = []
    for i, sp in enumerate(singleton_ports):
        result.append(sp % 256 ^ key_extended[i])
    
    print(f"\nXOR result (first 30 bytes): {bytes(result[:30])}")
    print(f"XOR result (hex): {bytes(result[:30]).hex()}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
