import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Vérifier l'entête ELF
assert data[:4] == b'\x7fELF', "Pas un ELF"
e_type = struct.unpack('<H', data[16:18])[0]
e_machine = struct.unpack('<H', data[18:20])[0]
e_entry = struct.unpack('<Q', data[24:32])[0]
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

print(f"Entry: 0x{e_entry:x}")
print(f"e_phoff: 0x{e_phoff:x}, e_phnum: {e_phnum}, e_phentsize: {e_phentsize}")

# Lire les program headers pour trouver le Segment 3
segments = []
for i in range(e_phnum):
    ph_offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
    p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
    p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
    p_paddr = struct.unpack('<Q', data[ph_offset+24:ph_offset+32])[0]
    p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
    p_memsz = struct.unpack('<Q', data[ph_offset+40:ph_offset+48])[0]
    p_flags = struct.unpack('<I', data[ph_offset+48:ph_offset+52])[0]
    p_align = struct.unpack('<Q', data[ph_offset+56:ph_offset+64])[0]
    segments.append({
        'type': p_type,
        'offset': p_offset,
        'vaddr': p_vaddr,
        'paddr': p_paddr,
        'filesz': p_filesz,
        'memsz': p_memsz,
        'flags': p_flags
    })
    print(f"Segment {i}: type={p_type}, vaddr=0x{p_vaddr:x}, offset=0x{p_offset:x}, filesz={p_filesz}, memsz={p_memsz}")

# Segment 3 devrait être le segment de données (type 1 = PT_LOAD)
# Trouver le segment qui contient vaddr 0x3da0
for i, seg in enumerate(segments):
    if seg['type'] == 1:  # PT_LOAD
        if seg['vaddr'] <= 0x3da0 < seg['vaddr'] + seg['memsz']:
            print(f"\nSegment contenant 0x3da0: segment {i}")
            print(f"  offset=0x{seg['offset']:x}, vaddr=0x{seg['vaddr']:x}")
            # Calculer l'offset de 0x3da0 dans ce segment
            offset_in_seg = 0x3da0 - seg['vaddr']
            file_offset = seg['offset'] + offset_in_seg
            print(f"  Offset fichier de 0x3da0: 0x{file_offset:x}")
            # Extraire les données à partir de 0x3da0
            bytecode_start = file_offset
            bytecode_data = data[bytecode_start:bytecode_start+256]
            print(f"  Bytecode (256 octets): {bytecode_data[:64].hex()}")