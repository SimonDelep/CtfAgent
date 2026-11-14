#!/usr/bin/env python3
from scapy.all import *
import struct

packets = rdpcap("capture.pcapng")

# Session 1: Server Hello est le paquet 11 (port 443 -> 60437)
# Session 2: Server Hello est le paquet 42 (port 4433 -> 60438)

def extract_server_random(pkt_idx):
    pkt = packets[pkt_idx]
    if Raw in pkt:
        data = bytes(pkt[Raw].load)
        # TLS Header: content_type(1) + version(2) + length(2)
        # Record Layer
        content_type = data[0]
        version = data[1:3]
        length = struct.unpack("!H", data[3:5])[0]
        
        print(f"Paquet {pkt_idx}: content_type=0x{content_type:02x}, version=0x{version.hex()}, length={length}")
        
        # Handshake Protocol starts at offset 5
        # Handshake Header: type(1) + length(3) + version(2) + random(32)
        if len(data) > 5:
            handshake_data = data[5:]
            handshake_type = handshake_data[0]
            handshake_length = struct.unpack("!I", b"\x00" + handshake_data[1:4])[0]
            handshake_version = handshake_data[4:6]
            print(f"  Handshake type: {handshake_type}, length: {handshake_length}, version: 0x{handshake_version.hex()}")
            
            if handshake_type == 2:  # Server Hello
                # Server Hello structure: version(2) + random(32) + ...
                server_random = handshake_data[6:38]  # 32 bytes after version
                print(f"  Server Random: {server_random.hex()}")
                return server_random
    return None

print("=== Session 1 (paquet 11) ===")
sr1 = extract_server_random(11)

print("\n=== Session 2 (paquet 42) ===")
sr2 = extract_server_random(42)
