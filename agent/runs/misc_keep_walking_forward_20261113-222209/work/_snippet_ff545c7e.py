from scapy.all import *
import sys
sys.path.insert(0, '/tmp/py7zr_pkg')

packets = rdpcap('capture.pcapng')

# Trouver tous les paquets TCP avec Raw data
tls_packets = []
for i, pkt in enumerate(packets):
    if TCP in pkt and Raw in pkt:
        raw_data = bytes(pkt[Raw])
        # Vérifier si c'est du TLS (Content Type en premier byte)
        if len(raw_data) > 0 and raw_data[0] in [0x16, 0x17, 0x15, 0x14, 0x13, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20]:
            content_type = raw_data[0]
            tls_packets.append((i, pkt, raw_data, content_type))
            print(f"Packet {i}: TLS Content Type 0x{content_type:02x}")
            print(f"  Raw data (first 100 bytes): {raw_data[:100].hex()}")
            print()