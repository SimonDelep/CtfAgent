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

# Extraire toutes les séquences
pos_22 = [pkt[22] for pkt in packets]
pos_24 = [pkt[24] for pkt in packets]
pos_34 = [pkt[34] for pkt in packets]
pos_35 = [pkt[35] for pkt in packets]

# Paquets état B
state_b = [(i, pkt) for i, pkt in enumerate(packets) if pkt[22] == 113]

print("Analyse des paquets état B:")
print(f"Nombre: {len(state_b)}")

# Regardons les variations dans pos_34 pour les paquets état B
pos_34_b = [pkt[34] for i, pkt in state_b]
from collections import Counter
print(f"\nDistribution de pos_34 dans état B: {Counter(pos_34_b)}")

# Et pos_24
pos_24_b = [pkt[24] for i, pkt in state_b]
print(f"Distribution de pos_24 dans état B: {Counter(pos_24_b)}")

# Peut-être que pos_34 ou pos_24 est la clé pour XOR pos_35
# Essayons pos_35 XOR pos_34 pour les paquets état B
print("\n\nXOR(pos_35, pos_34) pour état B:")
xored_34 = [pkt[35] ^ pkt[34] for i, pkt in state_b]
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in xored_34[:100]))

# Et pos_35 XOR pos_24
print("\nXOR(pos_35, pos_24) pour état B:")
xored_24 = [pkt[35] ^ pkt[24] for i, pkt in state_b]
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in xored_24[:100]))

# Et pos_35 XOR (pos_34 + pos_24) ou autre combinaison
print("\nXOR(pos_35, pos_34 ^ pos_24) pour état B:")
xored_combo = [pkt[35] ^ pkt[34] ^ pkt[24] for i, pkt in state_b]
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in xored_combo[:100]))