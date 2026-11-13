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

# Essayons différentes combinaisons de XOR
# Peut-être que pos_35 XOR pos_22 XOR pos_24 XOR pos_34 donne quelque chose

# D'abord, regardons si pos_35 contient des caractères ASCII quand on XOR avec une constante
# Ou peut-être que le message est dans les paquets où pos_35 a des valeurs spécifiques

# Regardons les valeurs de pos_35 qui apparaissent peu de fois - ce sont peut-être les "vrais" bits du message
from collections import Counter
pos_35_counts = Counter(pos_35)

# Les valeurs qui apparaissent 1 ou 2 fois pourraient être le signal
rare_values = {val: count for val, count in pos_35_counts.items() if count <= 3}
print(f"Valeurs rares de pos_35 (count <= 3): {rare_values}")

# Extraire les indices où pos_35 a des valeurs rares
rare_indices = [i for i, v in enumerate(pos_35) if pos_35_counts[v] <= 3]
print(f"Indices avec valeurs rares: {rare_indices[:30]}")

# Regardons les valeurs de pos_35 à ces indices
print("\nValeurs de pos_35 aux indices rares:")
for idx in rare_indices[:30]:
    print(f"  idx={idx}: pos_35=0x{pos_35[idx]:02x} ({pos_35[idx]}), pos_22={pos_22[idx]}, pos_24={pos_24[idx]}, pos_34={pos_34[idx]}")

# Peut-être que le message est simplement la séquence de pos_35 filtrée
# Ou peut-être que pos_35 XOR pos_22 donne le message
print("\n\nXOR(pos_35, pos_22) pour les indices rares:")
for idx in rare_indices[:30]:
    xored = pos_35[idx] ^ pos_22[idx]
    print(f"  idx={idx}: {pos_35[idx]:02x} ^ {pos_22[idx]:02x} = {xored:02x} ({chr(xored) if 32 <= xored < 127 else '.'})")