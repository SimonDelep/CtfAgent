from scapy.all import *
import sys
sys.path.insert(0, '/tmp/py7zr_pkg')

packets = rdpcap('capture.pcapng')

# Chercher "DOWNGRD" dans les données brutes
for i, pkt in enumerate(packets):
    if Raw in pkt:
        raw_data = bytes(pkt[Raw])
        if b'DOWNGRD' in raw_data or b'OWNGRD' in raw_data:
            print(f"Packet {i}: Found DOWNGRD")
            print(f"  Raw: {raw_data.hex()}")
            # Chercher la position de DOWNGRD
            pos = raw_data.find(b'DOWNGRD')
            if pos == -1:
                pos = raw_data.find(b'OWNGRD')
            print(f"  Position: {pos}")
            print(f"  Context: {raw_data[max(0,pos-20):pos+30]}")
            print()