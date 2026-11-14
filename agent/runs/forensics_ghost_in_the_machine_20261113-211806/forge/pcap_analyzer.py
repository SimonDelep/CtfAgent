SCHEMA = {
  "name": "pcap_analyzer",
  "description": "Analyse un fichier pcap custom avec marqueurs deadbeef, extrait ports sources, identifie singletons et ports fréquents, dérive une clé et tente de décrypter le message",
  "parameters": {
    "properties": {
      "key_from_frequent": {
        "description": "Utiliser les ports fréquents comme clé XOR",
        "type": "boolean"
      },
      "pcap_file": {
        "description": "Chemin du fichier pcap",
        "type": "string"
      }
    },
    "type": "object"
  }
}

def main(args):
    import struct
    
    pcap_file = args.get('pcap_file', 'capture.pcap')
    key_from_frequent = args.get('key_from_frequent', True)
    
    with open(pcap_file, 'rb') as f:
        data = f.read()
    
    # Magic number du fichier: c4c3b2a1 (4 octets)
    # En-tête global: 40 octets
    # Puis paquets délimités par deadbeef
    
    # Trouver tous les marqueurs deadbeef
    marker = b'\xde\xad\xbe\xef'
    positions = []
    pos = 0
    while True:
        idx = data.find(marker, pos)
        if idx == -1:
            break
        positions.append(idx)
        pos = idx + 1
    
    # Chaque paquet a la structure: deadbeef (4) + ? (2) + deadbeef (4) + données
    # Les positions sont les débuts des marqueurs deadbeef
    
    # Extraire les paquets UDP
    # Format custom: deadbeef + 2 octets + deadbeef + données
    # Les données contiennent l'en-tête IP (20 octets) + UDP (8 octets) + payload
    
    singletons = []
    frequent_ports = []
    port_counts = {}
    packet_order = []  # (position, port_source)
    
    # On suppose que les paquets commencent après le premier deadbeef
    # Le premier deadbeef est à position 44 (40 octets header + 4 octets deadbeef)
    # Vérifions la structure
    
    # Trouver le premier deadbeef après l'en-tête global (40 octets)
    first_deadbeef_after_header = None
    for i, pos in enumerate(positions):
        if pos >= 40:
            first_deadbeef_after_header = pos
            break
    
    if first_deadbeef_after_header is None:
        return "Pas de deadbeef trouvé après l'en-tête"
    
    # Parser chaque paquet
    # Structure: deadbeef (4) + 2 octets inconnus + deadbeef (4) + données
    # Les données contiennent IP header (20 octets) + UDP header (8 octets) + payload
    
    idx = 0
    packet_num = 0
    while idx < len(data) - 10:
        # Chercher deadbeef
        if data[idx:idx+4] == marker:
            # deadbeef trouvé, sauter 2 octets, chercher le deuxième deadbeef
            if idx + 6 < len(data) and data[idx+6:idx+10] == marker:
                # Données commencent à idx + 10
                data_start = idx + 10
                
                # Lire l'en-tête IP (20 octets)
                if data_start + 20 <= len(data):
                    ip_header = data[data_start:data_start+20]
                    
                    # IP header length (IHL) est sur l'octet 0, 4 bits supérieurs
                    ihl = (ip_header[0] & 0x0F) * 4
                    
                    # Port source à l'offset 20 + 2 (UDP header: port source 2 octets, port dest 2 octets)
                    # IP header commence à data_start, UDP header commence à data_start + 20 (si IHL=20)
                    udp_start = data_start + 20
                    
                    if udp_start + 4 <= len(data):
                        port_source = struct.unpack('>H', data[udp_start:udp_start+2])[0]
                        port_dest = struct.unpack('>H', data[udp_start+2:udp_start+4])[0]
                        
                        packet_order.append((packet_num, port_source))
                        
                        if port_source in port_counts:
                            port_counts[port_source] += 1
                        else:
                            port_counts[port_source] = 1
                
                # Passer au prochain paquet: chercher le prochain deadbeef
                idx = data_start + 10
                packet_num += 1
            else:
                idx += 1
        else:
            idx += 1
    
    # Identifier singletons et ports fréquents
    singleton_ports = []
    frequent_port_list = []
    
    for port, count in port_counts.items():
        if count == 1:
            singleton_ports.append(port)
        else:
            frequent_port_list.append((port, count))
    
    # Trier singletons par ordre d'apparition
    singleton_ports_ordered = [port for _, port in packet_order if port in singleton_ports]
    
    # Trier ports fréquents par ordre d'apparition
    frequent_ports_ordered = []
    seen = set()
    for _, port in packet_order:
        if port in frequent_port_list and port not in seen:
            frequent_ports_ordered.append(port)
            seen.add(port)
    
    # Extraire la clé des ports fréquents
    # Hypothèse: soustraire 40000 pour obtenir la clé ASCII
    key_chars = []
    for port in frequent_ports_ordered:
        char_val = port - 40000
        if 32 <= char_val < 127:
            key_chars.append(chr(char_val))
    
    key = ''.join(key_chars)
    
    # Décrypter les singletons avec XOR
    decrypted = []
    key_bytes = [ord(c) for c in key]
    key_len = len(key_bytes)
    
    for i, port in enumerate(singleton_ports_ordered):
        byte_val = port % 256
        if key_len > 0:
            decrypted_byte = byte_val ^ key_bytes[i % key_len]
        else:
            decrypted_byte = byte_val
        decrypted.append(decrypted_byte)
    
    # Essayer de convertir en string
    try:
        decrypted_str = bytes(decrypted).decode('utf-8', errors='replace')
    except:
        decrypted_str = str(decrypted)
    
    return f"""
Ports singletons (ordre d'apparition): {singleton_ports_ordered[:20]}... ({len(singleton_ports_ordered)} total)
Ports fréquents (ordre d'apparition): {frequent_ports_ordered}
Clé dérivée: '{key}'
Décrypté (XOR avec clé): {decrypted_str[:50]}...
"""

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
