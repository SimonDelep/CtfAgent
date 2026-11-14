from capstone import *

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Fonction pour convertir adresse virtuelle en offset fichier
# Pour un binaire non-PIE, l'offset est: addr - 0x400000 + offset_du_segment
# Mais on peut aussi utiliser les headers de section

# Trouver le segment LOAD qui contient l'adresse
e_phoff = 0x40
e_phentsize = 0x38
e_phnum = 13

# Lire les headers de programme pour trouver le mapping
for i in range(e_phnum):
    ph_offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
    if p_type == 1:  # PT_LOAD
        p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
        p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
        p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
        p_memsz = struct.unpack('<Q', data[ph_offset+40:ph_offset+48])[0]
        print(f"LOAD: offset=0x{p_offset:x}, vaddr=0x{p_vaddr:x}, filesz=0x{p_filesz:x}")

# Pour un ELF non-PIE, l'adresse virtuelle de base est généralement 0x400000
# Donc addr -> offset = addr - 0x400000 + offset_du_segment
# Mais en pratique, pour les segments LOAD, l'offset fichier = p_offset + (addr - p_vaddr)

def vaddr_to_offset(vaddr):
    for i in range(e_phnum):
        ph_offset = e_phoff + i * e_phentsize
        p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
        if p_type == 1:
            p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
            p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
            p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
            if p_vaddr <= vaddr < p_vaddr + p_filesz:
                return p_offset + (vaddr - p_vaddr)
    return None

# Désassembler main à 0x4011d6
main_vaddr = 0x4011d6
main_offset = vaddr_to_offset(main_vaddr)
print(f"main offset: 0x{main_offset:x}")

# Extraire le code de main (environ 200 octets pour voir la logique)
code_size = 300
code = data[main_offset:main_offset + code_size]

# Désassembler avec capstone
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

print("\n=== Désassemblage de main ===")
for insn in md.disasm(code, main_vaddr):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")