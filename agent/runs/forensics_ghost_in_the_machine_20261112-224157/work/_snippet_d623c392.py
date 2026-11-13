import struct

# Lire le fichier pcap
with open('capture_fixed.pcap', 'rb') as f:
    data = f.read()

# Parser tous les paquets
offset = 24
packets = []
timestamps = []

while offset < len(data):
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    if incl_len == 0 or incl_len > 1000:
        break
    packet_data = data[offset+16:offset+16+incl_len]
    packets.append(packet_data)
    timestamps.append((ts_sec, ts_usec))
    offset += 16 + incl_len

# Analyser les timestamps
print("Analyse des timestamps:")
for i in range(min(20, len(timestamps))):
    print(f"Paquet {i}: ts={timestamps[i][0]}.{timestamps[i][1]:06d}")

# Calculer les deltas
deltas = []
for i in range(1, len(timestamps)):
    delta_us = (timestamps[i][0] - timestamps[i-1][0]) * 1000000 + (timestamps[i][1] - timestamps[i-1][1])
    deltas.append(delta_us)

print(f"\nDeltas (premier 20): {deltas[:20]}")
print(f"Delta min: {min(deltas)}, max: {max(deltas)}")

# Peut-être que les paquets avec des deltas spécifiques sont le signal
# Ou peut-être que certains paquets ont des valeurs "normales" et d'autres sont le signal

# Regardons la distribution des valeurs à pos_35
from collections import Counter
pos_35_counts = Counter([pkt[35] for pkt in packets])
print(f"\nDistribution de pos_35 (top 20):")
for val, count in pos_35_counts.most_common(20):
    print(f"  0x{val:02x} ({val:3d}): {count} fois")

# La valeur la plus commune est probablement le "bruit"
most_common = pos_35_counts.most_common(1)[0][0]
print(f"\nValeur la plus commune: 0x{most_common:02x} ({most_common})")

# Extraire seulement les paquets où pos_35 != valeur la plus commune
signal_packets = [(i, pkt) for i, pkt in enumerate(packets) if pkt[35] != most_common]
print(f"Nombre de paquets 'signal': {len(signal_packets)} sur {len(packets)}")

# Regardons ces paquets
print("\nPaquets signal (premier 20):")
for idx, pkt in signal_packets[:20]:
    print(f"  Paquet {idx}: pos_35=0x{pkt[35]:02x} ({pkt[35]}), pos_22=0x{pkt[22]:02x} ({pkt[22]}), pos_24=0x{pkt[24]:02x} ({pkt[24]}), pos_34=0x{pkt[34]:02x} ({pkt[34]})")