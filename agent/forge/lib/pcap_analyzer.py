SCHEMA = {
  "name": "pcap_analyzer",
  "description": "Analyse un fichier pcap UDP, extrait les ports sources, identifie singletons et ports fréquents, et tente de décoder le message",
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
    "required": [
      "pcap_file"
    ],
    "type": "object"
  }
}

from scapy.all import rdpcap, UDP
from collections import Counter

def main(args):
    pcap_file = args.get('pcap_file', 'capture.pcap')
    use_key = args.get('key_from_frequent', True)
    
    packets = rdpcap(pcap_file)
    udp_packets = [p for p in packets if UDP in p]
    
    # Extraire ports sources dans l'ordre
    src_ports = [(i, p[UDP].sport) for i, p in enumerate(udp_packets)]
    
    # Compter occurrences
    port_counts = Counter([sport for _, sport in src_ports])
    
    # Séparer singletons et fréquents
    singletons = [(idx, port) for idx, port in src_ports if port_counts[port] == 1]
    frequent_ports = [(idx, port) for idx, port in src_ports if port_counts[port] > 1]
    
    print(f"Total paquets UDP: {len(udp_packets)}")
    print(f"Singletons: {len(singletons)}")
    print(f"Ports fréquents: {len(frequent_ports)}")
    
    # Afficher les ports fréquents uniques
    unique_frequent = sorted(set(port for _, port in frequent_ports))
    print(f"\nPorts fréquents uniques ({len(unique_frequent)}): {unique_frequent}")
    
    # Afficher les singletons dans l'ordre
    singleton_ports = [port for _, port in singletons]
    print(f"\nPremiers 20 singletons (ordre chronologique): {singleton_ports[:20]}")
    
    # Tenter de décoder avec XOR si clé fournie
    if use_key and unique_frequent:
        # Essayer de dériver une clé des ports fréquents
        # Soustraire un offset pour obtenir des valeurs ASCII
        key_candidates = []
        for offset in [40000, 40001, 40002]:
            key = ''.join(chr(port - offset) if 32 <= port - offset < 127 else '?' for port in sorted(unique_frequent))
            key_candidates.append((offset, key))
        
        print(f"\nClés candidates (ports fréquents - offset):")
        for offset, key in key_candidates:
            print(f"  offset={offset}: '{key}'")
        
        # Tenter XOR avec chaque clé candidate
        for offset, key in key_candidates:
            if all(32 <= ord(c) < 127 for c in key):
                key_bytes = [ord(c) for c in key]
                decrypted = []
                for i, port in enumerate(singleton_ports):
                    byte_val = port % 256
                    key_byte = key_bytes[i % len(key_bytes)]
                    decrypted.append(byte_val ^ key_byte)
                
                try:
                    result = ''.join(chr(b) if 32 <= b < 127 else '?' for b in decrypted)
                    print(f"\nDécryptage avec clé '{key}': {result[:80]}...")
                except:
                    pass
    
    return singletons, unique_frequent

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
