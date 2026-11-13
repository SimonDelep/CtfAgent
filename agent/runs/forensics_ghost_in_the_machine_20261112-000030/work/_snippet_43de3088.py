from scapy.all import *
packets = rdpcap("capture.pcap")
print(f"Total packets: {len(packets)}")
for i, pkt in enumerate(packets[:10]):
    print(f"Packet {i}: {pkt.summary()}")