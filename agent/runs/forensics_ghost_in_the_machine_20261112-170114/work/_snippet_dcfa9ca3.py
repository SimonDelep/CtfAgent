# Analyser le PCAP sans scapy - lire l'en-tête PCAP
with open("capture.pcap", "rb") as f:
    data = f.read()

# En-tête PCAP (24 octets)
magic = int.from_bytes(data[0:4], 'little')
print(f"Magic number: {hex(magic)}")
print(f"Version majeur: {int.from_bytes(data[4:6], 'little')}")
print(f"Version mineur: {int.from_bytes(data[6:8], 'little')}")
print(f"Data link type: {int.from_bytes(data[20:24], 'little')}")

# Chaque paquet a un en-tête de 16 octets (ts_sec, ts_usec, incl_len, orig_len)
# Puis les données du paquet
offset = 24
packets = []
while offset < len(data):
    ts_sec = int.from_bytes(data[offset:offset+4], 'little')
    ts_usec = int.from_bytes(data[offset+4:offset+8], 'little')
    incl_len = int.from_bytes(data[offset+8:offset+12], 'little')
    orig_len = int.from_bytes(data[offset+12:offset+16], 'little')
    pkt_data = data[offset+16:offset+16+incl_len]
    packets.append((ts_sec, ts_usec, incl_len, orig_len, pkt_data))
    offset += 16 + incl_len

print(f"\nNombre de paquets: {len(packets)}")
print(f"Taille totale: {len(data)} octets")