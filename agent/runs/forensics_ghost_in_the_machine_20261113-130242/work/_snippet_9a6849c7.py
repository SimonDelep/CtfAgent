import struct

with open('capture.pcap', 'rb') as f:
    data = f.read()

# Le header PCAP fait 24 octets
pcap_header = data[:24]
print(f"Header PCAP: {pcap_header.hex()}")

# Après le header, on devrait avoir les paquets
# Chaque paquet a un header de 16 octets (timestamp sec, usec, len_incl, len_orig)
# Puis les données du paquet

# Chercher la première occurrence de deadbeef après le header
idx = data.find(b'\xde\xad\xbe\xef', 24)
print(f"Premier deadbeef à l'offset: {idx}")

# Regarder autour de ce deadbeef
print(f"Contexte autour du deadbeef: {data[idx-10:idx+30].hex()}")
