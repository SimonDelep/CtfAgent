import sys
sys.path.insert(0, '/tmp/scapy_lib')
from scapy.all import *
from scapy.layers.tls.all import *
import binascii

# Lire le pcap
packets = rdpcap('capture.pcapng')

# Chercher les paquets avec des données chiffrées (Application Data)
for i, pkt in enumerate(packets):
    if TLS in pkt:
        tls_layer = pkt[TLS]
        # Afficher le type de contenu TLS
        if hasattr(tls_layer, 'type'):
            if tls_layer.type == 22:  # Handshake
                pass  # Déjà décrypté
            elif tls_layer.type == 23:  # Application Data
                print(f"Paquet {i}: Application Data chiffré")
                print(f"  Raw load: {tls_layer.msg}")
                print()