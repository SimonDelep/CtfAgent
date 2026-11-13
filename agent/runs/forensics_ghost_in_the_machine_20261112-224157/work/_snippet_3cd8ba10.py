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

# Regardons les valeurs de pos_34 et pos_24
print("\nAnalyse de pos_34 et pos_24:")
for idx, pkt in etat_b[:20]:
    print(f"Paquet {idx}: pos_24={pkt[24]}, pos_34={pkt[34]}, pos_35={pkt[35]}")

# Peut-être que la clé est pos_34 XOR pos_24?
print("\nXOR(pos_35, pos_34):")
for idx, pkt in etat_b[:20]:
    decoded = pkt[35] ^ pkt[34]
    print(f"Paquet {idx}: pos_35={pkt[35]}, pos_34={pkt[34]}, XOR={decoded} ({chr(decoded) if 32 <= decoded < 127 else '?'})")

# Ou peut-être que pos_34 est la clé et pos_35 est le ciphertext?
# Essayons XOR(pos_35, pos_34)
print("\nXOR(pos_35, pos_34) pour tous les paquets État B:")
decoded_chars = []
for idx, pkt in etat_b:
    decoded = pkt[35] ^ pkt[34]
    decoded_chars.append(decoded)

flag_attempt = ''.join(chr(c) if 32 <= c < 127 else '?' for c in decoded_chars)
print(f"Flag attempt: {flag_attempt}")