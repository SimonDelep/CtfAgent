from capstone import *
import struct

# Lire le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# Fonction pour convertir adresse virtuelle en offset fichier
e_phoff = 0x40
e_phentsize = 0x38
e_phnum = 13

# Trouver le segment LOAD qui contient l'adresse
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

# Extraire le code de main (environ 300 octets)
code_size = 300
code = data[main_offset:main_offset + code_size]

# Désassembler avec capstone
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

print("\n=== Désassemblage de main ===")
for insn in md.disasm(code, main_vaddr):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")