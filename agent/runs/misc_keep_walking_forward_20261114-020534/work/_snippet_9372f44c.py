from scapy.all import rdpcap, TCP, Raw
import struct

packets = rdpcap('capture.pcapng')

# Trouver les Server Hello et extraire les Server Randoms
for i, pkt in enumerate(packets):
    if TCP in pkt and Raw in pkt:
        payload = bytes(pkt[Raw].load)
        if len(payload) >= 43 and payload[0] == 0x16:  # Handshake
            # Handshake record: type(1) + version(2) + length(2) + handshake
            # Server Hello: type=0x02
            if len(payload) >= 5:
                handshake_type = payload[5]
                if handshake_type == 0x02:  # Server Hello
                    server_version = struct.unpack('>H', payload[6:8])[0]
                    server_random = payload[43:75]
                    print(f"Paquet {i}: Server Hello, version=0x{server_version:04x}")
                    print(f"  Server Random: {server_random.hex()}")
                    # Vérifier si contient "DOWNGRD" = 444f574e475244
                    if b'DOWNGRD' in server_random or b'GRD' in server_random:
                        print(f"  -> Contient DOWNGRD!")