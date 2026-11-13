# Essayons avec dpkt
try:
    import dpkt
    with open('capture.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        packets = list(pcap)
    print(f"Total packets: {len(packets)}")
    
    # Extraire les ports sources UDP
    ports = []
    for ts, buf in packets:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.ip
            udp = ip.udp
            ports.append(udp.sport)
        except:
            pass
    
    print(f"Total UDP ports extraits: {len(ports)}")
    
    from collections import Counter
    counts = Counter(ports)
    print(f"Nombre de ports uniques: {len(counts)}")
    
    # Ports fréquents (>=60 occurrences)
    frequent = [p for p, c in counts.items() if c >= 60]
    print(f"Ports fréquents: {sorted(frequent)}")
    
    # Singletons (1 occurrence)
    singletons = [p for p, c in counts.items() if c == 1]
    print(f"Nombre de singletons: {len(singletons)}")
    
    # Singletons dans l'ordre d'apparition
    singleton_order = []
    seen = set()
    for p in ports:
        if counts[p] == 1 and p not in seen:
            singleton_order.append(p)
            seen.add(p)
    
    print(f"\nSingletons dans l'ordre d'apparition (first 20): {singleton_order[:20]}")
    print(f"Total singletons dans l'ordre: {len(singleton_order)}")
    
    # La clé mod 256
    key_mod256 = [p % 256 for p in [40115, 40104, 40052, 40100, 40111, 40119]]
    print(f"\nClé mod 256: {key_mod256}")
    
    # XOR des singletons (mod 256) avec la clé cyclique
    singleton_mod256 = [s % 256 for s in singleton_order]
    result = bytes([s ^ key_mod256[i % 6] for i, s in enumerate(singleton_mod256)])
    print(f"\nXOR result (first 50): {result[:50]}")
    print(f"XOR result (hex): {result[:50].hex()}")
    
except ImportError:
    print("dpkt pas installé, essayons autre chose")