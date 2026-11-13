SCHEMA = {
  "name": "pcap_parser",
  "description": "Parse un fichier pcap manuellement (magic 0xa1b2c3c4) pour extraire les paquets UDP, identifie les ports sources fréquents et singletons",
  "parameters": {
    "properties": {
      "pcap_file": {
        "description": "Chemin du fichier pcap",
        "type": "string"
      }
    },
    "required": [
      "pcap_file"
    ],
    "type": "object"
  }
}

import struct
from collections import Counter

def main(args):
    pcap_file = args['pcap_file']
    
    with open(pcap_file, 'rb') as f:
        # Magic number (4 bytes) - devrait être 0xa1b2c3c4 en little-endian
        magic = struct.unpack('<I', f.read(4))[0]
        print(f"Magic number: 0x{magic:08x}")
        
        # Version majeure (2 bytes)
        major = struct.unpack('<H', f.read(2))[0]
        # Version mineure (2 bytes)
        minor = struct.unpack('<H', f.read(2))[0]
        print(f"Version: {major}.{minor}")
        
        # Timezone (4 bytes)
        tz = struct.unpack('<I', f.read(4))[0]
        # Timestamp accuracy (4 bytes)
        ts_acc = struct.unpack('<I', f.read(4))[0]
        # Snap length (4 bytes)
        snap_len = struct.unpack('<I', f.read(4))[0]
        # Link layer type (4 bytes)
        link_type = struct.unpack('<I', f.read(4))[0]
        print(f"Link type: {link_type}, Snap len: {snap_len}")
        
        # Parser les paquets
        packets = []
        while True:
            # Timestamp (4 bytes sec, 4 bytes usec)
            ts_sec = f.read(4)
            if len(ts_sec) < 4:
                break
            ts_usec = f.read(4)
            ts_sec = struct.unpack('<I', ts_sec)[0]
            ts_usec = struct.unpack('<I', ts_usec)[0]
            timestamp = ts_sec + ts_usec / 1000000.0
            
            # Longueur du paquet (4 bytes)
            incl_len = struct.unpack('<I', f.read(4))[0]
            orig_len = struct.unpack('<I', f.read(4))[0]
            
            # Données du paquet
            pkt_data = f.read(incl_len)
            
            # Parser l'en-tête Ethernet (14 bytes) puis IP (20 bytes) puis UDP (8 bytes)
            # Link type 1 = Ethernet
            if link_type == 1:
                # Ethernet header: 14 bytes
                eth_header = pkt_data[:14]
                ip_start = 14
            else:
                # Link type 228 = Linux SLL (cooked)
                if link_type == 228:
                    ip_start = 16
                else:
                    ip_start = 0
            
            # IP header
            if len(pkt_data) > ip_start + 20:
                ip_header = pkt_data[ip_start:ip_start+20]
                version_ihl = ip_header[0]
                ihl = (version_ihl & 0x0f) * 4
                protocol = ip_header[9]
                ip_src = '.'.join(str(b) for b in ip_header[12:16])
                ip_dst = '.'.join(str(b) for b in ip_header[16:20])
                
                # UDP
                if protocol == 17:
                    udp_start = ip_start + ihl
                    if len(pkt_data) > udp_start + 8:
                        udp_header = pkt_data[udp_start:udp_start+8]
                        sport = struct.unpack('>H', udp_header[0:2])[0]
                        dport = struct.unpack('>H', udp_header[2:4])[0]
                        udp_len = struct.unpack('>H', udp_header[4:6])[0]
                        udp_checksum = struct.unpack('>H', udp_header[6:8])[0]
                        
                        # Payload UDP
                        payload_start = udp_start + 8
                        payload = pkt_data[payload_start:payload_start+udp_len-8]
                        
                        packets.append({
                            'timestamp': timestamp,
                            'sport': sport,
                            'dport': dport,
                            'payload': payload,
                            'ip_src': ip_src,
                            'ip_dst': ip_dst
                        })
    
    print(f"\nTotal paquets UDP: {len(packets)}")
    
    # Analyser les ports sources
    src_ports = [p['sport'] for p in packets]
    port_counts = Counter(src_ports)
    
    frequent_ports = sorted([p for p, c in port_counts.items() if c > 1])
    singleton_ports = sorted([p for p, c in port_counts.items() if c == 1])
    
    print(f"Ports fréquents ({len(frequent_ports)}): {frequent_ports}")
    print(f"Singletons ({len(singleton_ports)}): {singleton_ports}")
    
    # Extraire les singletons triés par timestamp
    singleton_packets = [p for p in packets if p['sport'] in singleton_ports]
    singleton_packets.sort(key=lambda x: x['timestamp'])
    
    print(f"\nNombre de singletons: {len(singleton_packets)}")
    print("\n10 premiers singletons (timestamp, sport, dport, payload):")
    for sp in singleton_packets[:10]:
        print(f"  ts={sp['timestamp']:.6f}, sport={sp['sport']}, dport={sp['dport']}, payload={sp['payload']}")
    
    # Afficher les ports de destination des singletons
    singleton_dports = set(p['dport'] for p in singleton_packets)
    print(f"\nPorts de destination des singletons: {singleton_dports}")
    
    # Afficher les payloads des singletons
    print("\nPayloads des singletons:")
    for sp in singleton_packets:
        print(f"  sport={sp['sport']}: {sp['payload']}")
    
    return {
        'frequent_ports': frequent_ports,
        'singleton_ports': singleton_ports,
        'singleton_packets': singleton_packets
    }

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
