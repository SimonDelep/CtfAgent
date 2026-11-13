import sys
sys.path.insert(0, '/home/etudiantelambda/.local/lib/python3.12/site-packages')
from scapy.all import *

# Lire le pcapng
packets = rdpcap("capture.pcapng")

# Extraire les ClientRandom des paquets TLS (ClientHello)
# Le ClientRandom est dans le ClientHello message

def extract_client_random(p):
    """Extrait le ClientRandom d'un paquet TLS ClientHello"""
    if not p.haslayer(TCP):
        return None
    if not p.haslayer(Raw):
        return None
    
    data = bytes(p[Raw])
    # TLS record layer: content_type(1) + version(2) + length(2) + payload
    if len(data) < 5:
        return None
    
    content_type = data[0]
    if content_type != 0x16:  # Handshake
        return None
    
    # Skip TLS record header (5 bytes)
    offset = 5
    if offset >= len(data):
        return None
    
    # Handshake header: type(1) + length(3)
    handshake_type = data[offset]
    if handshake_type != 0x01:  # ClientHello
        return None
    
    # Skip handshake header (4 bytes)
    offset += 4
    if offset + 32 > len(data):
        return None
    
    # ClientRandom is 32 bytes
    client_random = data[offset:offset+32]
    return client_random.hex()

# Trouver les ClientRandom dans les paquets
client_randoms = {}
for i, p in enumerate(packets):
    if p.haslayer(TCP) and p.haslayer(Raw):
        cr = extract_client_random(p)
        if cr:
            # Identifier le flux
            if p.haslayer(TCP):
                src_port = p[TCP].sport
                dst_port = p[TCP].dport
                print(f"Paquet {i}: ClientRandom={cr}, port {src_port} -> {dst_port}")
                if dst_port == 443:
                    client_randoms['443'] = cr
                elif dst_port == 4433:
                    client_randoms['4433'] = cr

print(f"\nClientRandoms trouvés:")
for port, cr in client_randoms.items():
    print(f"  Port {port}: {cr}")