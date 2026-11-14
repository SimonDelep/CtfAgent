from scapy.all import *
import binascii

packets = rdpcap('capture.pcapng')

# Trouver les paquets TLS (port 443)
tls_packets = []
for i, pkt in enumerate(packets):
    if pkt.haslayer('TCP') and pkt.haslayer('Raw'):
        tcp = pkt['TCP']
        if tcp.dport == 443 or tcp.sport == 443:
            raw = bytes(pkt['Raw'].load)
            if len(raw) >= 5:
                content_type = raw[0]
                version = raw[1:3]
                if content_type in [0x16, 0x17, 0x14, 0x15]:  # TLS types
                    tls_packets.append((i, content_type, raw))

print(f"Paquets TLS trouvés: {len(tls_packets)}")
for idx, content_type, raw in tls_packets[:30]:
    type_name = {0x14: 'ChangeCipherSpec', 0x15: 'Alert', 0x16: 'Handshake', 0x17: 'ApplicationData'}.get(content_type, f'Unknown({content_type})')
    print(f"Paquet {idx}: type={type_name}, len={len(raw)}, hex={binascii.hexlify(raw[:40]).decode()}")