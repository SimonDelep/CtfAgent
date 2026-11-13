SCHEMA = {
  "name": "pcap_extractor",
  "description": "Extrait les paquets UDP d'un fichier pcap, identifie les ports sources fréquents et singletons, et retourne les données des singletons triés par timestamp",
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

from scapy.all import rdpcap, UDP
from collections import Counter

def main(args):
    pcap_file = args['pcap_file']
    
    # Charger le pcap
    packets = rdpcap(pcap_file)
    
    # Extraire les paquets UDP
    udp_packets = [p for p in packets if UDP in p]
    
    # Analyser les ports sources
    src_ports = [p[UDP].sport for p in udp_packets]
    port_counts = Counter(src_ports)
    
    # Ports fréquents (plusieurs occurrences)
    frequent_ports = sorted([p for p, c in port_counts.items() if c > 1])
    # Singletons (une seule occurrence)
    singleton_ports = sorted([p for p, c in port_counts.items() if c == 1])
    
    # Pour chaque singleton, extraire plus d'infos
    singleton_packets = []
    for i, p in enumerate(udp_packets):
        if p[UDP].sport in singleton_ports:
            singleton_packets.append({
                'index': i,
                'sport': p[UDP].sport,
                'dport': p[UDP].dport,
                'payload': bytes(p[UDP].payload),
                'time': float(p.time)
            })
    
    # Trier par timestamp
    singleton_packets.sort(key=lambda x: x['time'])
    
    # Retourner les informations
    result = {
        'total_udp': len(udp_packets),
        'frequent_ports': frequent_ports,
        'singleton_ports': singleton_ports,
        'singleton_count': len(singleton_packets),
        'singleton_data': [(sp['sport'], sp['dport'], sp['payload'], sp['time']) for sp in singleton_packets]
    }
    
    print(f"Total UDP: {result['total_udp']}")
    print(f"Ports fréquents ({len(frequent_ports)}): {frequent_ports}")
    print(f"Singletons ({len(singleton_ports)}): {singleton_ports}")
    print(f"Nombre de singletons: {result['singleton_count']}")
    
    # Afficher les 10 premiers singletons
    print("\n10 premiers singletons (sport, dport, payload):")
    for sp in singleton_packets[:10]:
        print(f"  sport={sp['sport']}, dport={sp['dport']}, payload={sp['payload']}")
    
    return result

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
