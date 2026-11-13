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
etat_b = [(idx, pkt) for idx, (ts, usec, pkt) in enumerate(packets) if pkt[22] == 113]

# La clé pourrait être 156 (valeur constante de pos_34 dans l'État A)
key = 156

print(f"XOR(pos_35, {key}):")
decoded_chars = []
for idx, pkt in etat_b:
    decoded = pkt[35] ^ key
    decoded_chars.append((idx, decoded))
    if len(decoded_chars) <= 30:
        print(f"Paquet {idx}: pos_35={pkt[35]}, XOR={decoded} ({chr(decoded) if 32 <= decoded < 127 else '?'})")

flag_attempt = ''.join(chr(c) if 32 <= c < 127 else '?' for _, c in decoded_chars)
print(f"\nFlag attempt: {flag_attempt}")