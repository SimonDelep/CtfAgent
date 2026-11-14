import capstone

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Entrée à 0x1230, mais c'est une adresse virtuelle.
# Pour un PIE, l'adresse virtuelle = offset dans le fichier (car load segment à 0x0)
# Vérifions les segments LOAD

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

# Désassembler à partir de l'offset correspondant à 0x1230
# Pour un PIE, l'adresse virtuelle est relative au chargement.
# Si le segment LOAD commence à 0x0, alors offset = adresse virtuelle.

# D'abord, trouvons l'offset du segment LOAD qui contient 0x1230
import struct

# Lire les en-têtes de programme
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]
e_phnum = struct.unpack('<H', data[0x38:0x3A])[0]

print(f"e_phoff: {e_phoff}, e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")

# Parcourir les segments LOAD
for i in range(e_phnum):
    phoff = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[phoff:phoff+4])[0]
    p_offset = struct.unpack('<Q', data[phoff+8:phoff+16])[0]
    p_vaddr = struct.unpack('<Q', data[phoff+16:phoff+24])[0]
    p_filesz = struct.unpack('<Q', data[phoff+32:phoff+40])[0]
    p_memsz = struct.unpack('<Q', data[phoff+40:phoff+48])[0]
    
    if p_type == 1:  # PT_LOAD
        print(f"LOAD: offset={hex(p_offset)}, vaddr={hex(p_vaddr)}, filesz={hex(p_filesz)}")
        # Vérifier si 0x1230 est dans ce segment
        if p_vaddr <= 0x1230 < p_vaddr + p_filesz:
            offset_in_segment = 0x1230 - p_vaddr
            file_offset = p_offset + offset_in_segment
            print(f"  -> 0x1230 est dans ce segment, offset fichier = {hex(file_offset)}")