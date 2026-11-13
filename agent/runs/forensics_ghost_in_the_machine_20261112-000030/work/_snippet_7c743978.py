import struct

# Re-lisons le pcap pour analyser la structure
with open('capture.pcap', 'rb') as f:
    data = f.read()

# Skip PCAP global header (24 bytes)
offset = 24

packets = []
while offset < len(data):
    # PCAP packet header: ts_sec(4) + ts_usec(4) + incl_len(4) + orig_len(4) = 16 bytes
    if offset + 16 > len(data):
        break
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', data[offset:offset+16])
    offset += 16
    
    if offset + incl_len > len(data):
        break
    
    pkt_data = data[offset:offset+incl_len]
    offset += incl_len
    
    packets.append(pkt_data)

# Analysons le premier paquet en détail
pkt = packets[0]
print(f"Longueur paquet: {len(pkt)}")
print(f"Hex dump complet:")
for i in range(0, len(pkt), 16):
    hex_part = ' '.join(f'{b:02x}' for b in pkt[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in pkt[i:i+16])
    print(f"{i:04x}: {hex_part:<48} {ascii_part}")

# Cherchons "PING" qui est mentionné dans la description
ping_pos = pkt.find(b'PING')
print(f"\n'PING' trouvé à: {ping_pos}")
if ping_pos >= 0:
    print(f"Contexte autour de PING: {pkt[ping_pos-10:ping_pos+20]}")