import struct

# Re-lisons le pcap pour analyser la structure
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Skip PCAP global header (24 bytes)
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
    
    packets.append(pkt_data)

# Cherchons "Se" dans tous les paquets
for i, pkt in enumerate(packets):
    se_pos = pkt.find(b'Se')
    if se_pos >= 0:
        print(f"Packet {i}: 'Se' à position {se_pos}")
        print(f"  Contexte: {pkt[se_pos-5:se_pos+15]}")
        if se_pos + 6 <= len(pkt):
            four_bytes = pkt[se_pos+2:se_pos+6]
            print(f"  4 octets après 'Se': {four_bytes.hex()} = {list(four_bytes)}")
        break

# Si pas de "Se", cherchons d'autres motifs
print("\nRecherche de motifs dans le premier paquet:")
for pattern in [b'Se', b'se', b'SE', b'\\x00\\x02', b'\\x00\\x01']:
    pos = pkt.find(pattern)
    if pos >= 0:
        print(f"  '{pattern}' trouvé à {pos}")

# Regardons la structure IP/UDP
# Après l'en-tête Ethernet (14 bytes) + IP (20 bytes) + UDP (8 bytes) = 42 bytes
# Le payload UDP commence à l'offset 42
print(f"\nPayload UDP du premier paquet (à partir de l'offset 42):")
print(f"  {packets[0][42:].hex()}")
print(f"  ASCII: {packets[0][42:]}")