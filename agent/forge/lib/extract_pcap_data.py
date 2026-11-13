SCHEMA = {
  "name": "extract_pcap_data",
  "description": "Extrait les champs clés de chaque paquet UDP du fichier pcap et les affiche sous forme de tableau",
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

def main(args):
    pcap_file = args.get('pcap_file', 'capture_fixed.pcap')
    
    with open(pcap_file, 'rb') as f:
        # Skip global header (24 bytes)
        f.read(24)
        
        packets = []
        while True:
            # Read packet header (16 bytes)
            pkt_header = f.read(16)
            if len(pkt_header) < 16:
                break
            
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', pkt_header)
            pkt_data = f.read(incl_len)
            
            if len(pkt_data) < 42:  # Minimum Ethernet + IP + UDP
                continue
            
            # Ethernet header (14 bytes)
            eth_header = pkt_data[:14]
            ip_start = 14
            
            # IP header
            ip_header = pkt_data[ip_start:ip_start+20]
            ip_version_ihl = ip_header[0]
            ip_header_len = (ip_version_ihl & 0x0F) * 4
            ip_total_len = struct.unpack('>H', ip_header[2:4])[0]
            ip_proto = ip_header[9]
            src_ip = '.'.join(str(b) for b in ip_header[12:16])
            dst_ip = '.'.join(str(b) for b in ip_header[16:20])
            
            # UDP header starts after IP header
            udp_start = ip_start + ip_header_len
            udp_header = pkt_data[udp_start:udp_start+8]
            src_port = struct.unpack('>H', udp_header[0:2])[0]
            dst_port = struct.unpack('>H', udp_header[2:4])[0]
            udp_len = struct.unpack('>H', udp_header[4:6])[0]
            udp_checksum = struct.unpack('>H', udp_header[6:8])[0]
            
            # UDP data
            udp_data = pkt_data[udp_start+8:udp_start+8+udp_len-8]
            
            packets.append({
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'udp_len': udp_len,
                'udp_checksum': udp_checksum,
                'udp_data': udp_data,
                'ts_usec': ts_usec
            })
    
    # Print first 20 packets
    for i, p in enumerate(packets[:20]):
        print(f"Pkt {i}: src={p['src_ip']}:{p['src_port']} -> dst={p['dst_ip']}:{p['dst_port']}, udp_len={p['udp_len']}, checksum={p['udp_checksum']}, data={p['udp_data'].hex()}")
    
    print(f"\nTotal packets: {len(packets)}")
    
    # Analyze variations
    src_ports = set(p['src_port'] for p in packets)
    dst_ports = set(p['dst_port'] for p in packets)
    checksums = set(p['udp_checksum'] for p in packets)
    data_set = set(p['udp_data'] for p in packets)
    
    print(f"\nUnique src_ports: {len(src_ports)}")
    print(f"Unique dst_ports: {len(dst_ports)}")
    print(f"Unique checksums: {len(checksums)}")
    print(f"Unique data values: {len(data_set)}")
    
    # Show unique data values
    if len(data_set) > 1:
        print("\nUnique data values:")
        for d in data_set:
            print(f"  {d.hex()}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
