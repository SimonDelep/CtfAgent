# D'abord, trouvons l'entrée du programme et désassemblons le code x86-64
import struct

with open('masterkey', 'rb') as f:
    data = f.read()

# Lire l'entête ELF
e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
print(f"Entrée du programme: 0x{e_entry:x}")

# Trouver le segment LOAD qui contient l'entrée
# Les en-têtes de programme commencent à e_phoff (offset 0x20)
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]
e_phnum = struct.unpack('<H', data[0x38:0x3a])[0]

print(f"e_phoff: {e_phoff}, e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")

# Trouver le segment qui contient l'entrée
for i in range(e_phnum):
    ph_offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
    p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
    p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
    p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
    p_memsz = struct.unpack('<Q', data[ph_offset+40:ph_offset+48])[0]
    p_flags = struct.unpack('<I', data[ph_offset+24:ph_offset+28])[0]
    
    if p_type == 1:  # PT_LOAD
        # Vérifier si l'entrée est dans ce segment
        if p_vaddr <= e_entry < p_vaddr + p_memsz:
            print(f"\nSegment LOAD contenant l'entrée:")
            print(f"  p_offset: 0x{p_offset:x}")
            print(f"  p_vaddr: 0x{p_vaddr:x}")
            print(f"  p_filesz: {p_filesz}")
            print(f"  p_memsz: {p_memsz}")
            print(f"  p_flags: {p_flags}")
            
            # Extraire le code
            code_offset = p_offset + (e_entry - p_vaddr)
            code = data[code_offset:code_offset+500]
            print(f"\nCode à l'entrée (premier 200 octets):")
            for j in range(0, min(200, len(code)), 16):
                hex_part = ' '.join(f'{b:02x}' for b in code[j:j+16])
                ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in code[j:j+16])
                print(f"{code_offset+j:04x}: {hex_part:<48} {ascii_part}")