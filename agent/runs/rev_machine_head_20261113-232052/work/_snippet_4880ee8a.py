import struct
import capstone

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

# Regardons les chaînes de message
# "Wrong." est à 0x2010+
# "Correct! That's the master key." est à 0x2020+

# Trouvons les adresses exactes
wrong_offset = data.find(b'Wrong.')
correct_offset = data.find(b'Correct!')
print(f"Wrong. à offset {wrong_offset:#x}")
print(f"Correct! à offset {correct_offset:#x}")

# Convertir en adresse virtuelle
# .rodata est dans le segment à offset=0x2000, vaddr=0x2000
wrong_vaddr = 0x2000 + (wrong_offset - 0x2000) if wrong_offset >= 0x2000 else wrong_offset
correct_vaddr = 0x2000 + (correct_offset - 0x2000) if correct_offset >= 0x2000 else correct_offset
print(f"Wrong. vaddr: {wrong_vaddr:#x}")
print(f"Correct! vaddr: {correct_vaddr:#x}")

# Maintenant, regardons le code qui compare le flag
# La fonction principale semble être à 0x12d0, qui appelle 0x1260
# 0x1260 est un dispatcher

# Regardons ce qui se passe après l'appel à 0x1260 dans 0x12f7
# Après le call, il y a: mov byte ptr [rip + 0x2d25], 1

# [rip + 0x2d25] à 0x12fc: rip après = 0x1303, addr = 0x1303 + 0x2d25 = 0x4028

# Regardons ce qui se trouve à 0x4028
offset_4028 = vaddr_to_offset(0x4028)
print(f"\nOffset de 0x4028: {offset_4028}")

# 0x4028 est juste au-delà de 0x4010, donc hors du segment 3
# Peut-être que c'est dans un autre segment ou c'est de la mémoire dynamique

# Regardons le segment 3 plus en détail
print("\nSegment 3 (0x3da0 à 0x4010):")
for i in range(0, 0x270, 32):
    addr = 0x3da0 + i
    offset = 0x2da0 + i
    if offset + 32 <= len(data):
        hex_data = ' '.join(f'{b:02x}' for b in data[offset:offset+32])
        print(f"0x{addr:04x}: {hex_data}")