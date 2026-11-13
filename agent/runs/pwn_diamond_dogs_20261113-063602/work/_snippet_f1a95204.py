from capstone import *
import struct

md = Cs(CS_ARCH_X86, CS_MODE_64)

with open("guard-dog", "rb") as f:
    data = f.read()

# Parse ELF header to find program headers
e_phoff = struct.unpack("<Q", data[0x20:0x28])[0]
e_phentsize = struct.unpack("<H", data[0x36:0x38])[0]
e_phnum = struct.unpack("<H", data[0x38:0x3A])[0]

print(f"e_phoff={e_phoff}, e_phentsize={e_phentsize}, e_phnum={e_phnum}")

# Find the LOAD segment with executable flag
for i in range(e_phnum):
    offset = e_phoff + i * e_phentsize
    p_type = struct.unpack("<I", data[offset:offset+4])[0]
    p_flags = struct.unpack("<I", data[offset+4:offset+8])[0]
    p_offset = struct.unpack("<Q", data[offset+8:offset+16])[0]
    p_vaddr = struct.unpack("<Q", data[offset+16:offset+24])[0]
    p_filesz = struct.unpack("<Q", data[offset+32:offset+40])[0]
    
    if p_type == 1:  # PT_LOAD
        if p_flags & 1:  # executable
            print(f"Segment: vaddr=0x{p_vaddr:x}, offset=0x{p_offset:x}, filesz=0x{p_filesz:x}")
            # Disassemble this segment
            code = data[p_offset:p_offset+p_filesz]
            for insn in md.disasm(code, p_vaddr):
                print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")