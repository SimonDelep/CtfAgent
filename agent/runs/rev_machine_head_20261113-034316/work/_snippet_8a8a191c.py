import struct

with open('masterkey', 'rb') as f:
    data = f.read()

# Header ELF
e_type = struct.unpack('<H', data[0x10:0x12])[0]
e_machine = struct.unpack('<H', data[0x12:0x14])[0]
e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
e_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
e_phentsize = struct.unpack('<H', data[0x36:0x38])[0]
e_phnum = struct.unpack('<H', data[0x38:0x3a])[0]
e_shentsize = struct.unpack('<H', data[0x3a:0x3c])[0]
e_shnum = struct.unpack('<H', data[0x3c:0x3e])[0]
e_shstrndx = struct.unpack('<H', data[0x3e:0x40])[0]

print(f"e_type: {e_type} (3=executable)")
print(f"e_machine: {e_machine} (62=x86-64)")
print(f"e_entry: {hex(e_entry)}")
print(f"e_phoff: {hex(e_phoff)}")
print(f"e_shoff: {hex(e_shoff)}")
print(f"e_phentsize: {e_phentsize}, e_phnum: {e_phnum}")
print(f"e_shentsize: {e_shentsize}, e_shnum: {e_shnum}, e_shstrndx: {e_shstrndx}")

# Analyser les en-têtes de programme
print("\n=== Segments LOAD ===")
for i in range(e_phnum):
    offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[offset:offset+4])[0]
    p_flags = struct.unpack('<I', data[offset+24:offset+28])[0]
    p_offset = struct.unpack('<I', data[offset+4:offset+8])[0]
    p_vaddr = struct.unpack('<Q', data[offset+8:offset+16])[0]
    p_filesz = struct.unpack('<I', data[offset+16:offset+20])[0]
    p_memsz = struct.unpack('<I', data[offset+20:offset+24])[0]
    
    if p_type == 1:  # PT_LOAD
        print(f"LOAD: offset={hex(p_offset)}, vaddr={hex(p_vaddr)}, filesz={p_filesz}, memsz={p_memsz}, flags={p_flags}")