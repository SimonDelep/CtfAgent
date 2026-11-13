from scapy.all import *
import os

# Lire le pcapng
pcap_path = "/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/agent/runs/misc_keep_walking_forward_20261112-174941/work/capture.pcapng"
packets = rdpcap(pcap_path)

print(f"Nombre de paquets: {len(packets)}")

# Afficher les premiers paquets
for i, pkt in enumerate(packets[:10]):
    print(f"\n--- Paquet {i} ---")
    print(pkt.summary())