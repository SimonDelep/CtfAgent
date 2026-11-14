from scapy.all import rdpcap, TCP, Raw
import struct

packets = rdpcap('capture.pcapng')

# Trouver tous les paquets TLS et afficher leur structure
for i, pkt in enumerate(packets):
    if TCP in pkt and Raw in pkt:
        payload = bytes(pkt[Raw].load)
        if len(payload) >= 5:
            record_type = payload[0]
            version = struct.unpack('>H', payload[1:3])[0]
            length = struct.unpack('>H', payload[3:5])[0]
            
            type_names = {0x14: 'ChangeCipherSpec', 0x15: 'Alert', 0x16: 'Handshake', 0x17: 'Application Data'}
            type_name = type_names.get(record_type, f'0x{record_type:02x}')
            
            print(f"Paquet {i}: type={type_name} ({record_type}), version=0x{version:04x}, length={length}, payload_len={len(payload)}")
            
            if record_type == 0x17 and len(payload) >= 13:
                # Application Data: header(5) + explicit_nonce(8) + ciphertext + tag
                explicit_nonce = payload[5:13]
                print(f"  explicit_nonce: {explicit_nonce.hex()}")
                print(f"  ciphertext+tag: {payload[13:25].hex()}...")