SCHEMA = {
  "name": "extract_singletons",
  "description": "Extrait les paquets UDP d'un pcap, identifie les ports sources singletons (apparaissant une seule fois), et retourne les ports triés par timestamp",
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

def main(args):
    pcap_file = args["pcap_file"]
    
    with open(pcap_file, "rb") as f:
        # Magic number
        magic = f.read(4)
        if magic == b'\xa1\xb2\xc3\xd4':
            endian = '<'  # little-endian
        elif magic == b'\xd4\xc3\xb2\xa1':
            endian = '>'  # big-endian
        else:
            return f"Magic inconnu: {magic.hex()}"
        
        # Header PCAP (24 bytes)
        header = f.read(24)
        if len(header) < 24:
            return "Header trop court"
        
        version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack(endian + 'HHIIHH', header)
        
        packets = []
        while True:
            # Packet header: ts_sec, ts_usec, incl_len, orig_len (16 bytes)
            pkt_header = f.read(16)
            if len(pkt_header) < 16:
                break
            
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', pkt_header)
            pkt_data = f.read(incl_len)
            
            if len(pkt_data) < incl_len:
                break
            
            # Network type 1 = Ethernet
            if network == 1:
                eth_len = 14
            elif network == 228:  # LINKTYPE_IPV4
                eth_len = 0
            else:
                eth_len = 14
            
            if len(pkt_data) < eth_len + 28:
                continue
            
            if eth_len > 0:
                ip_start = eth_len
            else:
                ip_start = 0
            
            # IP header
            ip_header = pkt_data[ip_start:ip_start+20]
            if len(ip_header) < 20:
                continue
            
            version_ihl = ip_header[0]
            ihl = (version_ihl & 0x0F) * 4
            protocol = ip_header[9]
            
            if protocol != 17:  # UDP
                continue
            
            udp_start = ip_start + ihl
            udp_header = pkt_data[udp_start:udp_start+8]
            if len(udp_header) < 8:
                continue
            
            src_port, dst_port, length, checksum = struct.unpack('>HHHH', udp_header)
            
            packets.append({
                'ts': ts_sec + ts_usec / 1000000.0,
                'src_port': src_port,
                'dst_port': dst_port,
                'length': length
            })
    
    # Compter les occurrences de chaque port source
    port_counts = {}
    for pkt in packets:
        port = pkt['src_port']
        port_counts[port] = port_counts.get(port, 0) + 1
    
    # Identifier les singletons (port qui apparaît une seule fois)
    singleton_ports = {port for port, count in port_counts.items() if count == 1}
    frequent_ports = {port for port, count in port_counts.items() if count > 1}
    
    # Extraire les paquets avec des ports singletons, triés par timestamp
    singleton_packets = [pkt for pkt in packets if pkt['src_port'] in singleton_ports]
    singleton_packets.sort(key=lambda x: x['ts'])
    
    # Afficher les ports singletons et leurs fréquences
    result = f"Total paquets: {len(packets)}\n"
    result += f"Ports singletons: {len(singleton_ports)}\n"
    result += f"Ports fréquents: {len(frequent_ports)}\n"
    result += f"Ports fréquents (top 5): {[(p, port_counts[p]) for p in frequent_ports][:5]}\n"
    result += f"Singletons ports: {sorted(singleton_ports)[:20]}...\n"
    
    # Afficher la séquence des ports singletons triés par timestamp
    seq = [pkt['src_port'] for pkt in singleton_packets]
    result += f"Séquence des singletons (premiers 30): {seq[:30]}\n"
    
    # Essayer de convertir en ASCII
    # Option 1: port - 0xC000
    decoded1 = ''.join(chr(p - 0xC000) if 0 <= p - 0xC000 < 128 else '?' for p in seq)
    result += f"Décodage (port - 0xC000): {decoded1[:50]}\n"
    
    # Option 2: port - 0xC100
    decoded2 = ''.join(chr(p - 0xC100) if 0 <= p - 0xC100 < 128 else '?' for p in seq)
    result += f"Décodage (port - 0xC100): {decoded2[:50]}\n"
    
    # Option 3: port & 0xFF (bas octet)
    decoded3 = ''.join(chr(p & 0xFF) if 32 <= (p & 0xFF) < 127 else '.' for p in seq)
    result += f"Décodage (port & 0xFF): {decoded3[:50]}\n"
    
    # Option 4: port >> 8 (haut octet)
    decoded4 = ''.join(chr(p >> 8) if 32 <= (p >> 8) < 127 else '.' for p in seq)
    result += f"Décodage (port >> 8): {decoded4[:50]}\n"
    
    return result

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
