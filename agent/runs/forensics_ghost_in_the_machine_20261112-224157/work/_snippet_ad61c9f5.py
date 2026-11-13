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

# État B seulement
etat_b = []
for i, (ts, usec, pkt) in enumerate(packets):
    if pkt[22] == 113:
        etat_b.append((i, pkt))

print(f"État B: {len(etat_b)} paquets")

# Regardons les valeurs de pos_34
pos_34_values = [pkt[34] for _, pkt in etat_b]
print(f"Valeurs de pos_34: {pos_34_values[:30]}")

# Est-ce que pos_34 est un compteur séquentiel?
print(f"\nDifférences entre valeurs consécutives de pos_34:")
for i in range(1, min(20, len(pos_34_values))):
    diff = pos_34_values[i] - pos_34_values[i-1]
    print(f"  {pos_34_values[i-1]} -> {pos_34_values[i]} (diff={diff})")

# Peut-être que la clé est liée à pos_34?
# Essayons XOR(pos_35, pos_34 + quelque chose)
# Ou peut-être que la clé est pos_24 XOR pos_34?

print("\nXOR(pos_35, pos_24 XOR pos_34):")
decoded_chars = []
for idx, pkt in etat_b:
    key = pkt[24] ^ pkt[34]
    decoded = pkt[35] ^ key
    decoded_chars.append(decoded)
    if len(decoded_chars) <= 20:
        print(f"Paquet {idx}: pos_24={pkt[24]}, pos_34={pkt[34]}, key={key}, pos_35={pkt[35]}, XOR={decoded} ({chr(decoded) if 32 <= decoded < 127 else '?'})")

flag_attempt = ''.join(chr(c) if 32 <= c < 127 else '?' for c in decoded_chars)
print(f"\nFlag attempt: {flag_attempt}")