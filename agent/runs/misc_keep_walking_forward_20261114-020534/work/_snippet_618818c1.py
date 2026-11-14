from scapy.all import rdpcap, TCP, Raw
import struct

packets = rdpcap('capture.pcapng')

# Examinons le paquet 11 en détail
pkt = packets[11]
if TCP in pkt and Raw in pkt:
    payload = bytes(pkt[Raw].load)
    print(f"Longueur payload: {len(payload)}")
    print(f"Premiers 100 bytes: {payload[:100].hex()}")
    
    # Record TLS: type(1) + version(2) + length(2)
    record_type = payload[0]
    version = struct.unpack('>H', payload[1:3])[0]
    length = struct.unpack('>H', payload[3:5])[0]
    
    print(f"Record type: {record_type}, version: 0x{version:04x}, length: {length}")
    
    # Handshake: type(1) + length(3) + version(2) + random(32) + ...
    if len(payload) >= 43:
        handshake_type = payload[5]
        print(f"Handshake type: {handshake_type}")
        
        if handshake_type == 0x02:  # Server Hello
            handshake_version = struct.unpack('>H', payload[6:8])[0]
            server_random = payload[8:40]  # 32 bytes
            print(f"Handshake version: 0x{handshake_version:04x}")
            print(f"Server Random: {server_random.hex()}")