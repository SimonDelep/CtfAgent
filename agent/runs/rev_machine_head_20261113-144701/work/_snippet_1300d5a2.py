import capstone
import struct

binary_path = "masterkey"

# Lire le binaire
with open(binary_path, "rb") as f:
    data = f.read()

# Parser l'ELF
e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
e_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
e_shentsize = struct.unpack('<H', data[0x3a:0x3c])[0]
e_shnum = struct.unpack('<H', data[0x3c:0x3e])[0]

print(f"Entry point: {hex(e_entry)}")
print(f"Section header offset: {hex(e_shoff)}")
print(f"Number of sections: {e_shnum}")

# Trouver .text
text_offset = 0
text_size = 0
text_vaddr = 0

for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
    sh_offset_sec = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
    sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
    sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
    sh_flags = struct.unpack('<Q', data[sh_offset+40:sh_offset+48])[0]
    
    # SHT_PROGBITS (1) avec execute flag (SHF_EXECINSTR = 4)
    if sh_type == 1 and (sh_flags & 4):
        print(f"Found executable section at {hex(sh_addr)}, size {sh_size}, offset {hex(sh_offset_sec)}")
        if sh_addr <= e_entry < sh_addr + sh_size:
            text_offset = sh_offset_sec
            text_size = sh_size
            text_vaddr = sh_addr
            print(f"-> This is .text (contains entry point)")

print(f"\n.text: offset={hex(text_offset)}, size={text_size}, vaddr={hex(text_vaddr)}")

# Extraire et désassembler
if text_offset > 0:
    text_data = data[text_offset:text_offset+text_size]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False
    
    count = 0
    for insn in md.disasm(text_data, text_vaddr):
        print(f"{hex(insn.address)}: {insn.mnemonic} {insn.op_str}")
        count += 1
        if count >= 80:
            break