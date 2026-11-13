# Essayons d'utiliser scapy si disponible
try:
    from scapy.all import rdpcap, TCP, IP
    packets = rdpcap('fenwick_capture.pcap')
    print(f"Nombre total de paquets: {len(packets)}")
    
    # Filtrer les paquets TCP sur le port 8443
    heartbeat_packets = []
    for pkt in packets:
        if TCP in pkt and (pkt[TCP].dport == 8443 or pkt[TCP].sport == 8443):
            if TCP in pkt and pkt[TCP].payload:
                payload = bytes(pkt[TCP].payload)
                if payload:
                    heartbeat_packets.append((pkt.time, pkt[IP].src, pkt[IP].dst, pkt[TCP].sport, pkt[TCP].dport, payload))
    
    print(f"\nPaquets TCP avec payload sur le port 8443: {len(heartbeat_packets)}")
    
    for i, (ts, src, dst, sport, dport, payload) in enumerate(heartbeat_packets[:10]):
        print(f"\n--- Paquet {i+1} ---")
        print(f"Time: {ts}, {src}:{sport} -> {dst}:{dport}")
        try:
            text = payload.decode('utf-8', errors='replace')
            print(f"Payload: {text[:300]}")
        except:
            print(f"Payload (hex): {payload[:100].hex()}")
except ImportError:
    print("Scapy non disponible, essayons une approche manuelle")
except Exception as e:
    print(f"Erreur: {e}")