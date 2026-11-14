import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

def vaddr_to_offset(vaddr):
    if vaddr < 0x750:
        return vaddr
    elif 0x1000 <= vaddr < 0x1329:
        return vaddr
    elif 0x2000 <= vaddr < 0x28a0:
        return vaddr
    elif 0x3da0 <= vaddr < 0x4010:
        return 0x2da0 + (vaddr - 0x3da0)
    else:
        return None

# 0x4008 est juste à la limite du segment 3 (0x3da0 à 0x4010)
# 0x4008 < 0x4010, donc c'est dans le segment
offset_4008 = vaddr_to_offset(0x4008)
print(f"Offset de 0x4008: {offset_4008:#x}")

# Lisons autour de 0x4008
print("\nDonnées autour de 0x4008:")
for i in range(-16, 32, 16):
    addr = 0x4008 + i
    offset = vaddr_to_offset(addr)
    if offset and offset + 16 <= len(data):
        hex_data = ' '.join(f'{b:02x}' for b in data[offset:offset+16])
        ascii_data = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        print(f"0x{addr:04x} (offset {offset:#x}): {hex_data}  {ascii_data}")

# Regardons aussi la section .rodata qui devrait contenir les chaînes
# .rodata est probablement dans le segment à 0x2000
# Les chaînes "Wrong." et "Correct!" devraient être là

print("\n\nRecherche de chaînes dans .rodata (0x2000+):")
for i in range(0x2000, min(0x28a0, len(data)), 16):
    chunk = data[i:i+16]
    # Chercher des chaînes imprimables
    printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    if 'Wrong' in printable or 'Correct' in printable or 'key' in printable:
        print(f"0x{i:04x}: {printable}")