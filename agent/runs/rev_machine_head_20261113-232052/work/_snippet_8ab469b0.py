import capstone
import struct

# Lire le binaire
with open("masterkey", "rb") as f:
    data = f.read()

# Parser l'ELF pour trouver les sections
# Offset des sections
e_shoff = struct.unpack("<Q", data[40:48])[0]
e_shentsize = struct.unpack("<H", data[58:60])[0]
e_shnum = struct.unpack("<H", data[60:62])[0]
e_shstrndx = struct.unpack("<H", data[62:64])[0]

print(f"e_shoff: {hex(e_shoff)}, e_shentsize: {e_shentsize}, e_shnum: {e_shnum}")

# Trouver la section .text
text_offset = None
text_vaddr = None
text_size = None

rodata_offset = None
rodata_vaddr = None
rodata_size = None

for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh = data[sh_offset:sh_offset + e_shentsize]
    sh_name_idx = struct.unpack("<I", sh[0:4])[0]
    sh_type = struct.unpack("<I", sh[4:8])[0]
    sh_flags = struct.unpack("<Q", sh[8:16])[0]
    sh_addr = struct.unpack("<Q", sh[16:24])[0]
    sh_off = struct.unpack("<Q", sh[24:32])[0]
    sh_size = struct.unpack("<Q", sh[32:40])[0]
    
    # Lire le nom de la section depuis la table des chaînes
    # On a besoin de l'index de la table des chaînes
    if i == e_shstrndx:
        shstrtab_off = sh_off
        shstrtab_size = sh_size
    
    if sh_type == 1:  # SHT_PROGBITS
        # Lire le nom
        name_start = shstrtab_off + sh_name_idx
        name_end = name_start
        while name_end < shstrtab_off + shstrtab_size and data[name_end] != 0:
            name_end += 1
        name = data[name_start:name_end].decode("utf-8", errors="ignore")
        
        if name == ".text":
            text_offset = sh_off
            text_vaddr = sh_addr
            text_size = sh_size
            print(f".text: vaddr={hex(sh_addr)}, offset={hex(sh_off)}, size={sh_size}")
        elif name == ".rodata":
            rodata_offset = sh_off
            rodata_vaddr = sh_addr
            rodata_size = sh_size
            print(f".rodata: vaddr={hex(sh_addr)}, offset={hex(sh_off)}, size={sh_size}")

# Désassembler .text
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False

if text_offset:
    text_data = data[text_offset:text_offset + text_size]
    print("\n=== Code .text ===")
    for insn in md.disasm(text_data, text_vaddr):
        print(f"{hex(insn.address)}: {insn.mnemonic} {insn.op_str}")