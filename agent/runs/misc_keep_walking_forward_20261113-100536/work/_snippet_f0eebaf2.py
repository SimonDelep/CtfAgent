import sys
sys.path.insert(0, '/home/etudiantelambda/.local/lib/python3.12/site-packages')

from scapy.all import *
import binascii

# Charger le pcap
packets = rdpcap('capture.pcapng')

# Définir les sessions
session1_cr = "6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a"
session2_cr = "6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd"

# Session 1: port 443 (Client Hello au paquet 9)
# Session 2: port 4433 (Client Hello au paquet 40)

# Identifier les paquets de chaque session
# Session 1: paquets entre le Client Hello (paquet 9) et la fin de la session
# Session 2: paquets entre le Client Hello (paquet 40) et la fin

# Pour simplifier, identifions les paquets par port
# Session 1: port 443
# Session 2: port 4433

print("Analyse des paquets par session:")
print("\n--- Session 1 (port 443) ---")
for i, p in enumerate(packets):
    if TCP in p:
        if p[TCP].dport == 443 or p[TCP].sport == 443:
            payload_len = len(p[TCP].payload) if p[TCP].payload else 0
            print(f"Paquet {i}: sport={p[TCP].sport}, dport={p[TCP].dport}, payload_len={payload_len}")

print("\n--- Session 2 (port 4433) ---")
for i, p in enumerate(packets):
    if TCP in p:
        if p[TCP].dport == 4433 or p[TCP].sport == 4433:
            payload_len = len(p[TCP].payload) if p[TCP].payload else 0
            print(f"Paquet {i}: sport={p[TCP].sport}, dport={p[TCP].dport}, payload_len={payload_len}")