import pyshark

# Charger le pcap avec le fichier de clés SSL
cap = pyshark.FileCapture(
    'capture.pcapng',
    display_filter='http',
    decryption_key='sslkeylog.log'
)

# Afficher les paquets HTTP déchiffrés
for pkt in cap:
    print("=== Paquet HTTP ===")
    if hasattr(pkt, 'http'):
        print(f"HTTP Version: {pkt.http.get('http_version', 'N/A')}")
        print(f"Method: {pkt.http.get('method', 'N/A')}")
        print(f"Host: {pkt.http.get('host', 'N/A')}")
        print(f"URI: {pkt.http.get('uri', 'N/A')}")
        if hasattr(pkt, 'data'):
            print(f"Data: {pkt.data}")
    print()

cap.close()