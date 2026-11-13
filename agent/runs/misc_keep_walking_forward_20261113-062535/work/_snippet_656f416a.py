# Les ClientRandoms du PCAP (avec prefix de version)
cr_443_full = "03036aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0"
cr_4433_full = "03016aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798"

# Le vrai ClientRandom est après les 2 premiers bytes (version)
cr_443 = cr_443_full[4:]  # Skip "0303" (2 bytes = 4 hex chars)
cr_4433 = cr_4433_full[4:]  # Skip "0301"

print(f"ClientRandom pour port 443: {cr_443} (len={len(cr_443)})")
print(f"ClientRandom pour port 4433: {cr_4433} (len={len(cr_4433)})")

# Les clés du sslkeylog.txt
key1_cr = "6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a"
key2_cr = "6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd"

print(f"\nKey1 CR: {key1_cr} (len={len(key1_cr)})")
print(f"Key2 CR: {key2_cr} (len={len(key2_cr)})")

# Le ClientRandom TLS standard fait 32 bytes = 64 hex chars
# Nos extraits semblent plus courts
print(f"\nLongueur attendue: 64 hex chars")
print(f"cr_443 longueur: {len(cr_443)}")
print(f"cr_4433 longueur: {len(cr_4433)}")

# Peut-être que l'extraction a été tronquée - vérifions les paquets bruts
import sys
sys.path.insert(0, '/home/etudiantelambda/.local/lib/python3.12/site-packages')
from scapy.all import *

packets = rdpcap("capture.pcapng")

# Paquet 9 est le ClientHello pour port 443
p = packets[9]
if p.haslayer(Raw):
    data = bytes(p[Raw])
    print(f"\nDonnées brutes du paquet 9: {data.hex()}")
    print(f"Longueur: {len(data)}")
    
# Paquet 40 est le ClientHello pour port 4433
p = packets[40]
if p.haslayer(Raw):
    data = bytes(p[Raw])
    print(f"\nDonnées brutes du paquet 40: {data.hex()}")
    print(f"Longueur: {len(data)}")