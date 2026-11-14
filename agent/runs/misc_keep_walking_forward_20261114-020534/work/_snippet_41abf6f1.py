#!/usr/bin/env python3
"""
Analyser le Server Hello pour trouver le cipher suite
"""
from scapy.all import rdpcap, Raw

packets = rdpcap('capture.pcapng')

# Chercher le Server Hello (dans les paquets TLS)
for i, pkt in enumerate(packets):
    if Raw in pkt:
        raw = bytes(pkt[Raw].load)
        if len(raw) >= 5:
            content_type = raw[0]
            # TLS Handshake (22)
            if content_type == 0x16:
                # Vérifier si c'est un Server Hello
                # TLS Record: Type(1) + Version(2) + Length(2) + Handshake Type(1) + ...
                if len(raw) >= 10:
                    handshake_type = raw[5]
                    if handshake_type == 0x02:  # Server Hello
                        print(f"Paquet {i}: Server Hello")
                        print(f"  Raw (hex): {raw[:50].hex()}")
                        # Le Server Hello contient le cipher suite à offset 43 dans le handshake
                        # Structure: Handshake Type(1) + Length(3) + Version(2) + Random(32) + Session ID len(1) + Session ID + Cipher Suite(2) + Compression(1)
                        # Après le header TLS (5 bytes) + handshake type (1) + handshake length (3)
                        offset = 5 + 1 + 3  # 9 bytes pour aller au début du Server Hello body
                        version = raw[offset:offset+2]
                        random = raw[offset+2:offset+34]
                        session_id_len = raw[offset+34]
                        session_id = raw[offset+35:offset+35+session_id_len]
                        cipher_suite_offset = offset + 35 + session_id_len
                        cipher_suite = raw[cipher_suite_offset:cipher_suite_offset+2]
                        print(f"  Version: {version.hex()}")
                        print(f"  Random: {random.hex()}")
                        print(f"  Session ID len: {session_id_len}")
                        print(f"  Cipher Suite: {cipher_suite.hex()}")
                        break