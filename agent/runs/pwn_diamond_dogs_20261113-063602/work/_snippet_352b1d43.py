import capstone
import struct

# Charger le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Parser les headers ELF
e_machine = struct.unpack('<H', data[18:20])[0]
print(f"e_machine: {e_machine}")  # 0x3e = x86_64

# Pour x86_64
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

# Trouver l'adresse de base (PT_LOAD)
# Header ELF: e_phoff à l'offset 0x20
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]
e_phnum = struct.unpack('<H', data[0x38:0x3A])[0]

print(f"e_phoff: {e_phoff}, e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")

# Trouver le segment texte (PT_LOAD avec flags execute)
base_addr = None
text_offset = None
for i in range(e_phnum):
    phoff = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[phoff:phoff+4])[0]
    p_offset = struct.unpack('<Q', data[phoff+8:phoff+16])[0]
    p_vaddr = struct.unpack('<Q', data[phoff+16:phoff+24])[0]
    p_filesz = struct.unpack('<Q', data[phoff+32:phoff+40])[0]
    p_memsz = struct.unpack('<Q', data[phoff+40:phoff+48])[0]
    p_flags = struct.unpack('<I', data[phoff+4:phoff+8])[0]
    
    if p_type == 1:  # PT_LOAD
        if p_flags & 1:  # Execute flag
            base_addr = p_vaddr
            text_offset = p_offset
            print(f"Text segment: vaddr={hex(p_vaddr)}, offset={hex(p_offset)}, size={p_filesz}")

# Extraire la section .text
if base_addr and text_offset:
    # Trouver la taille de .text via les sections
    e_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
    e_shentsize = struct.unpack('<H', data[0x3A:0x3C])[0]
    e_shnum = struct.unpack('<H', data[0x3C:0x3E])[0]
    e_shstrndx = struct.unpack('<H', data[0x3E:0x40])[0]
    
    # Lire la chaîne de noms de sections
    shstrtab_offset = None
    for i in range(e_shnum):
        shoff = e_shoff + i * e_shentsize
        sh_name = struct.unpack('<I', data[shoff:shoff+4])[0]
        sh_type = struct.unpack('<I', data[shoff+4:shoff+8])[0]
        
        if i == e_shstrndx:
            shstrtab_offset = struct.unpack('<Q', data[shoff+24:shoff+32])[0]
    
    # Trouver .text
    text_size = 0
    for i in range(e_shnum):
        shoff = e_shoff + i * e_shentsize
        sh_name = struct.unpack('<I', data[shoff:shoff+4])[0]
        sh_type = struct.unpack('<I', data[shoff+4:shoff+8])[0]
        sh_offset = struct.unpack('<Q', data[shoff+24:shoff+32])[0]
        sh_size = struct.unpack('<Q', data[shoff+32:shoff+40])[0]
        sh_addr = struct.unpack('<Q', data[shoff+16:shoff+24])[0]
        
        # Lire le nom
        name_start = shstrtab_offset + sh_name
        name_end = data.find(b'\x00', name_start)
        name = data[name_start:name_end].decode('utf-8')
        
        if name == '.text':
            print(f".text: addr={hex(sh_addr)}, offset={hex(sh_offset)}, size={sh_size}")
            text_size = sh_size
            break
    
    # Désassembler main (0x401321)
    main_addr = 0x401321
    main_offset = text_offset + (main_addr - base_addr)
    print(f"\n=== Désassemblage de main à {hex(main_addr)} ===")
    
    code = data[main_offset:main_offset+2000]
    for insn in md.disasm(code, main_addr):
        print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")
        if insn.address > main_addr + 1200:
            break