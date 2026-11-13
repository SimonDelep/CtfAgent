from scapy.all import *

packets = rdpcap('capture.pcapng')
print(f"Nombre de paquets: {len(packets)}")

for i, pkt in enumerate(packets[:10]):
    print(f"Paquet {i}: {pkt.summary()}")
    if pkt.haslayer('Raw'):
        raw = bytes(pkt['Raw'])
        print(f"  Raw ({len(raw)} bytes): {raw[:60].hex()}")