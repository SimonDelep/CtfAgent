import pyshark

# Charger le pcap avec le fichier de clés SSL
cap = pyshark.FileCapture(
    'capture.pcapng',
    display_filter='tls',
    decryption_key='sslkeys.log',
    decryption_type='pre-master-log'
)

# Lire les paquets
for i, pkt in enumerate(cap):
    print(f"Paquet {i}:")
    try:
        if hasattr(pkt, 'tls'):
            print(f"  TLS Layer: {pkt.tls}")
        if hasattr(pkt, 'http'):
            print(f"  HTTP Layer: {pkt.http}")
        if hasattr(pkt, 'data'):
            print(f"  Data: {pkt.data}")
    except Exception as e:
        print(f"  Erreur: {e}")
    print()
    if i > 10:
        break