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

# Extraire les valeurs aux positions variables
pos_22 = [pkt[22] for pkt in packets]
pos_24 = [pkt[24] for pkt in packets]
pos_34 = [pkt[34] for pkt in packets]
pos_35 = [pkt[35] for pkt in packets]

print("Position 22 (2 valeurs):")
print(f"  Valeurs: {sorted(set(pos_22))}")
print(f"  Séquence (premier 20): {pos_22[:20]}")

print("\nPosition 24 (2 valeurs):")
print(f"  Valeurs: {sorted(set(pos_24))}")
print(f"  Séquence (premier 20): {pos_24[:20]}")

print("\nPosition 34 (6 valeurs):")
print(f"  Valeurs: {sorted(set(pos_34))}")
print(f"  Séquence (premier 20): {pos_34[:20]}")

print("\nPosition 35 (98 valeurs):")
print(f"  Valeurs uniques: {sorted(set(pos_35))}")
print(f"  Séquence (premier 50): {pos_35[:50]}")

# Essayons de convertir position 35 en ASCII
print("\n\nPosition 35 comme ASCII (premier 100):")
ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in pos_35[:100])
print(ascii_str)

# Peut-être que c'est XOR avec une clé ?
# Regardons si position 35 contient des caractères imprimables
imprimables = [b for b in pos_35 if 32 <= b < 127]
print(f"\nCaractères imprimables dans pos_35: {len(imprimables)} sur {len(pos_35)}")
print(f"Pourcentage: {100*len(imprimables)/len(pos_35):.1f}%")