import sys
sys.path.insert(0, '/home/etudiantelambda/.local/lib/python3.12/site-packages')

from scapy.all import *
import binascii

# Charger le pcap
packets = rdpcap('capture.pcapng')

# Fonction pour extraire le Client Random d'un Client Hello TLS
def extract_client_random_from_client_hello(payload):
    """
    Le Client Hello TLS a la structure:
    - Content Type (1 byte) = 22 (Handshake)
    - Version (2 bytes)
    - Length (2 bytes)
    - Handshake Type (1 byte) = 1 (Client Hello)
    - Length (3 bytes)
    - Version (2 bytes)
    - Random (32 bytes) <- C'est ce qu'on cherche
    """
    if len(payload) < 43:  # Minimum pour un Client Hello
        return None
    
    # Content type devrait être 22 (Handshake)
    if payload[0] != 22:
        return None
    
    # Handshake type devrait être 1 (Client Hello)
    # Offset: 1 (content type) + 2 (version) + 2 (length) = 5
    if payload[5] != 1:
        return None
    
    # Le Client Random commence à l'offset 5 + 1 (handshake type) + 3 (handshake length) + 2 (version) = 11
    client_random = payload[11:43]
    return client_random

# Parcourir les paquets TCP et chercher les Client Hello
client_randoms = []
for i, p in enumerate(packets):
    if TCP in p and Raw in p:
        payload = bytes(p[TCP].payload)
        if len(payload) > 0:
            # Vérifier si c'est un Client Hello
            cr = extract_client_random_from_client_hello(payload)
            if cr:
                client_randoms.append((i, cr.hex(), p[TCP].sport, p[TCP].dport))
                print(f"Paquet {i}: Client Hello trouvé, sport={p[TCP].sport}, dport={p[TCP].dport}")
                print(f"  Client Random: {cr.hex()}")

print(f"\nTotal Client Hello trouvés: {len(client_randoms)}")