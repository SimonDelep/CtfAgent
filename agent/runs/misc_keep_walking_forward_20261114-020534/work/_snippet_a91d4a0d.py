#!/usr/bin/env python3
"""
Analyser le contenu brut des paquets Application Data
"""
from scapy.all import rdpcap, Raw

packets = rdpcap('capture.pcapng')

print("Contenu brut des premiers paquets Application Data:")
count = 0
for i, pkt in enumerate(packets):
    if Raw in pkt:
        raw = bytes(pkt[Raw].load)
        if len(raw) >= 5 and raw[0] == 0x17:  # Application Data
            print(f"\n=== Paquet {i}, len={len(raw)} ===")
            print(f"Header (5 bytes): {raw[:5].hex()}")
            print(f"Bytes 5-20: {raw[5:20].hex()}")
            print(f"Premiers 50 bytes: {raw[:50].hex()}")
            # Essayer de décoder en ASCII
            try:
                text = raw.decode('ascii', errors='replace')
                print(f"ASCII: {text[:100]}")
            except:
                pass
            count += 1
            if count >= 3:
                break