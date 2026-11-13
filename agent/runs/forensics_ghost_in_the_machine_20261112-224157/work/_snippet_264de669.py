import struct

# Lire le fichier pcap
with open('capture_fixed.pcap', 'rb') as f:
    data = f.read()

# Parser tous les paquets
offset = 24
packets = []

while offset < len(data):
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    if incl_len == 0 or incl_len > 1000:
        break
    packet_data = data[offset+16:offset+16+incl_len]
    packets.append(packet_data)
    offset += 16 + incl_len

# Analyser la structure du paquet
# Les 8 premiers octets semblent être un marqueur "deadbeef..."
# Ensuite c'est probablement un en-tête Ethernet (14 octets) + IP + UDP

# En-tête Ethernet standard: 6 octets dest MAC, 6 octets src MAC, 2 octets type
# Mais ici on voit "deadbeef" qui n'est pas standard

# Regardons les positions 34 et 35 - ce sont probablement les ports UDP
# Dans un paquet IP/UDP:
# - Offset 0-13: Ethernet (14 octets)
# - Offset 14-33: IP (20 octets minimum)
# - Offset 34-35: Port source UDP (2 octets)
# - Offset 36-37: Port dest UDP (2 octets)
# - Offset 38-39: Longueur UDP (2 octets)
# - Offset 40-41: Checksum UDP (2 octets)
# - Offset 42+: Données UDP

# Mais nos paquets font 46 octets, donc:
# 46 - 14 (Ethernet) - 20 (IP) = 12 octets pour UDP
# UDP header = 8 octets, donc 4 octets de données

# Vérifions: position 34-35 = port source, 36-37 = port dest
# Position 34 est le byte high du port source, position 35 est le byte low

# Extraire les ports UDP
print("Analyse des ports UDP:")
for i in range(min(10, len(packets))):
    pkt = packets[i]
    # Port source: bytes 34-35 (big-endian)
    src_port = (pkt[34] << 8) | pkt[35]
    # Port dest: bytes 36-37
    dst_port = (pkt[36] << 8) | pkt[37]
    print(f"Paquet {i}: src_port={src_port} (0x{pkt[34]:02x}{pkt[35]:02x}), dst_port={dst_port} (0x{pkt[36]:02x}{pkt[37]:02x})")

# Maintenant, regardons si les variations dans pos_35 correspondent à quelque chose de significatif
# Peut-être que pos_35 contient le signal XORé avec une clé

# La clé serait dans une autre colonne (position)
# pos_22 a seulement 2 valeurs: 64 et 113
# pos_24 a seulement 2 valeurs: 152 et 201
# pos_34 a 6 valeurs

# Peut-être que la clé est dérivée de ces positions
print("\n\nExtraction de la séquence pos_35:")
pos_35_seq = [pkt[35] for pkt in packets]
print(f"Séquence pos_35 (premier 50): {pos_35_seq[:50]}")

# Et pos_22 comme clé potentielle
pos_22_seq = [pkt[22] for pkt in packets]
print(f"Séquence pos_22 (premier 50): {pos_22_seq[:50]}")

# XOR pos_35 avec pos_22
xored = [pos_35_seq[i] ^ pos_22_seq[i] for i in range(len(packets))]
print(f"\nXOR(pos_35, pos_22) (premier 50): {xored[:50]}")
print(f"XOR comme ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in xored[:100])}")