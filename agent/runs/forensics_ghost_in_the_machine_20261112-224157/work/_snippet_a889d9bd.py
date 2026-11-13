import struct

# Lire le PCAP
with open('capture.pcap', 'rb') as f:
    data = f.read()

offset = 24
packets = []
while offset < len(data):
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append((ts_sec, ts_usec, pkt_data))

# Séparer les paquets en État A et État B
etat_a = []
etat_b = []

for i, (ts, usec, pkt) in enumerate(packets):
    if pkt[22] == 64:
        etat_a.append((i, pkt))
    elif pkt[22] == 113:
        etat_b.append((i, pkt))

print(f"État A (bruit): {len(etat_a)} paquets")
print(f"État B (signal): {len(etat_b)} paquets")

# Pour l'État B, calculer XOR(pos_35, pos_24)
print("\nÉtat B - XOR(pos_35, pos_24):")
decoded_chars = []
for idx, pkt in etat_b:
    pos_24 = pkt[24]
    pos_35 = pkt[35]
    decoded = pos_35 ^ pos_24
    decoded_chars.append(decoded)
    print(f"Paquet {idx}: pos_24={pos_24}, pos_35={pos_35}, XOR={decoded} ({chr(decoded) if 32 <= decoded < 127 else '?'})")

# Concaténer les caractères décodés
flag_attempt = ''.join(chr(c) if 32 <= c < 127 else '?' for c in decoded_chars)
print(f"\nFlag attempt: {flag_attempt}")