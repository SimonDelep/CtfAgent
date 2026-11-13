import sys
sys.path.insert(0, './scapy_lib')

# Essayer d'installer pytls ou utiliser une approche simple
# D'abord, vérifions si ssl est disponible
import ssl
print("SSL module disponible")

# Les clés pré-maîtres
pre_master_secrets = [
    ("6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a", "7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05"),
    ("6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd", "4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a63307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c")
]

# Le premier ClientRandom dans le PCAP est 6aa4f15c...
# Donc on utilise la première clé

# Pour décrypter TLS 1.3, on a besoin de:
# - ClientRandom
# - PreMasterSecret
# - Puis dériver les clés

# Essayons d'utiliser la bibliothèque tls ou faire manuellement
# D'abord, extrayons les enregistrements TLS

def parse_tls_records(data):
    records = []
    i = 0
    while i < len(data):
        if i + 5 > len(data):
            break
        content_type = data[i]
        version = data[i+1:i+3]
        length = int.from_bytes(data[i+3:i+5], 'big')
        if i + 5 + length > len(data):
            break
        record_data = data[i+5:i+5+length]
        records.append((content_type, version, length, record_data))
        i += 5 + length
    return records

# Lire les données
from scapy.all import *
packets = rdpcap('capture.pcapng')

tcp_stream = []
for p in packets:
    if TCP in p and p.haslayer(Raw):
        if p[TCP].dport == 443 or p[TCP].sport == 443:
            tcp_stream.append(p)

all_data = b''
for p in tcp_stream:
    raw_data = bytes(p[Raw].load)
    all_data += raw_data

records = parse_tls_records(all_data)
print(f"Nombre d'enregistrements TLS: {len(records)}")

# Afficher les types de contenu
content_types = {0x14: 'ChangeCipherSpec', 0x15: 'Alert', 0x16: 'Handshake', 0x17: 'Application Data'}
for i, (ct, ver, length, data) in enumerate(records[:10]):
    ct_name = content_types.get(ct, f'Unknown({ct})')
    print(f"Record {i}: type={ct_name}, version={ver.hex()}, length={length}")