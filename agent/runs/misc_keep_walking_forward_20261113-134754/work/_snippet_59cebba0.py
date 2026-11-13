import struct

with open("capture.pcapng", 'rb') as f:
    data = f.read()

# Regardons autour de la position 136
print("Autour de pos=136:")
for i in range(128, 160, 4):
    val = struct.unpack('<I', data[i:i+4])[0]
    print(f"  pos={i}: {hex(val)} = {val}")

# Le premier paquet finit à pos=133 (24+16+93=133), padding de 3 octets -> 136
# Vérifions les octets de padding
print(f"\nOctets de padding (133-135): {data[133:136].hex()}")

# Regardons ce qui est à partir de 136
print(f"\nDonnées à partir de 136: {data[136:180].hex()}")

# Peut-être que le format est différent. Vérifions si c'est pcapng au lieu de pcap
# pcapng a des blocks avec type(4) + len(4)
print(f"\nVérification pcapng à pos=136:")
if len(data) > 140:
    block_type = struct.unpack('<I', data[136:140])[0]
    block_len = struct.unpack('<I', data[140:144])[0]
    print(f"  block_type={hex(block_type)}, block_len={block_len}")

# Le magic pcapng est 0x0A0D0D0A (little-endian) ou 0x28057234
# Regardons le début du fichier
print(f"\nMagic pcapng attendu: 0x0A0D0D0A")
print(f"Magic actuel: {hex(struct.unpack('<I', data[0:4])[0])}")

# Peut-être que le fichier est en fait pcapng et pas pcap
# pcapng Section Header Block: type=0x0A0D0D0A, len=28 + options
print(f"\nAnalyse pcapng:")
pos = 0
while pos < min(500, len(data)):
    block_type = struct.unpack('<I', data[pos:pos+4])[0]
    block_len = struct.unpack('<I', data[pos+4:pos+8])[0]
    print(f"pos={pos}: block_type={hex(block_type)}, block_len={block_len}")
    if block_type == 0x0A0D0D0A:
        print("  -> Section Header Block")
    elif block_type == 0x00000001:
        print("  -> End of Section")
    elif block_type == 0x00000006:
        print("  -> Interface Description Block")
    elif block_type == 0x00000007:
        print("  -> Simple Packet Block")
    elif block_type == 0x00000008:
        print("  -> Enhanced Packet Block")
    else:
        print(f"  -> Block inconnu")
    
    # Avancer
    if block_len > 0 and block_len < 100000:
        pos += block_len
        if block_len % 8 != 0:
            pos += 8 - (block_len % 8)
    else:
        pos += 8  # Avancer de 8 pour éviter boucle infinie
        if pos > 500:
            break
