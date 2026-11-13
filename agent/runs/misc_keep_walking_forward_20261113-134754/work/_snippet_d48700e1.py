from scapy.all import *
from scapy.layers.tls.all import *
import binascii

# Charger le pcap
packets = rdpcap("capture.pcapng")

# Lire les secrets TLS
secrets = {}
with open("sslkey.log", "r") as f:
    for line in f:
        if line.startswith("CLIENT_RANDOM"):
            parts = line.strip().split()
            client_random = parts[1]
            master_secret = parts[2]
            secrets[client_random] = master_secret

print(f"Secrets chargés: {len(secrets)}")
for cr, ms in secrets.items():
    print(f"  CR: {cr[:16]}... MS: {ms[:16]}...")

# Analyser les paquets TLS
for i, pkt in enumerate(packets):
    if TCP in pkt and Raw in pkt:
        # Vérifier si c'est du TLS
        if pkt[TCP].dport == 443 or pkt[TCP].sport == 443:
            raw_data = bytes(pkt[Raw].load)
            if len(raw_data) > 0:
                # Type de contenu TLS (premier octet)
                content_type = raw_data[0]
                print(f"Paquet {i}: port={pkt[TCP].sport}->{pkt[TCP].dport}, type={content_type}, len={len(raw_data)}")
                if content_type == 22:  # Handshake
                    print(f"  -> Handshake")
                elif content_type == 23:  # Application Data
                    print(f"  -> Application Data (chiffré)")
                elif content_type == 16:  # Change Cipher Spec
                    print(f"  -> Change Cipher Spec")
                elif content_type == 20:  # Alert
                    print(f"  -> Alert")
                else:
                    print(f"  -> Type inconnu")
