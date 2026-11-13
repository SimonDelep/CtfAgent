from scapy.all import *

# Lire le pcap
packets = rdpcap('capture.pcapng')

print(f"Total packets: {len(packets)}")

# Analyser chaque paquet
for i, pkt in enumerate(packets):
    if TCP in pkt:
        src = f"{pkt[IP].src}:{pkt[TCP].sport}"
        dst = f"{pkt[IP].dst}:{pkt[TCP].dport}"
        flags = str(pkt[TCP].flags)
        
        if Raw in pkt:
            data = bytes(pkt[Raw].load)
            # Afficher les premières lignes
            if i < 10:
                print(f"Packet {i}: {src} -> {dst} [{flags}]")
                print(f"  Data (hex): {data[:60].hex()}")
                print(f"  Data (ascii): {data[:60]}")
        else:
            if i < 10:
                print(f"Packet {i}: {src} -> {dst} [{flags}] (no raw)")