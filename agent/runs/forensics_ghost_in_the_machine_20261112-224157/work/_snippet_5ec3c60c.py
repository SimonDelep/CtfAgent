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

# Séparer les paquets par état
state_a = [(i, pkt) for i, pkt in enumerate(packets) if pkt[22] == 64]  # pos_22 = 0x40
state_b = [(i, pkt) for i, pkt in enumerate(packets) if pkt[22] == 113]  # pos_22 = 0x71

print(f"État A (pos_22=64): {len(state_a)} paquets")
print(f"État B (pos_22=113): {len(state_b)} paquets")

# Regardons la séquence d'états
states = ['A' if p[22] == 64 else 'B' for p in packets]
print(f"\nSéquence d'états (premier 50): {''.join(states[:50])}")

# Peut-être que l'état indique un bit (0 ou 1) et pos_35 est le message
# Ou peut-être que pos_35 XOR quelque chose donne le message selon l'état

# Essayons: si état A, pos_35 XOR 64; si état B, pos_35 XOR 113
decoded = []
for i, pkt in enumerate(packets):
    if pkt[22] == 64:
        decoded.append(pkt[35] ^ 64)
    else:
        decoded.append(pkt[35] ^ 113)

print(f"\nDécodé (XOR selon état): {''.join(chr(b) if 32 <= b < 127 else '.' for b in decoded[:100])}")

# Peut-être que le message est seulement dans les paquets d'un certain état
print("\n\nPos_35 XOR 64 pour les paquets état A:")
a_decoded = [pkt[35] ^ 64 for i, pkt in state_a]
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in a_decoded[:100]))

print("\nPos_35 XOR 113 pour les paquets état B:")
b_decoded = [pkt[35] ^ 113 for i, pkt in state_b]
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in b_decoded[:100]))