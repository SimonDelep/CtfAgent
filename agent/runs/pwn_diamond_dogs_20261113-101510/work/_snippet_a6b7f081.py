from capstone import *
import struct

# Lire le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Trouver l'entrée
# ELF header: e_entry à l'offset 0x18
e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
print(f"Entry point: 0x{e_entry:x}")

# Load address pour un EXEC non-PIE est généralement 0x400000
# Mais vérifions les segments
for i in range(struct.unpack('<H', data[0x3c:0x3e])[0]):  # e_phnum
    ph_offset = struct.unpack('<H', data[0x3e:0x40])[0]  # e_phoff
    ph_entry_size = struct.unpack('<H', data[0x3a:0x3c])[0]  # e_phentsize
    ph_offset = struct.unpack('<H', data[0x3e:0x40])[0]
    
# Trouver le segment de code
for i in range(struct.unpack('<H', data[0x3a:0x3c])[0]):
    ph_offset = struct.unpack('<H', data[0x3e:0x40])[0]
    ph_entry_offset = ph_offset + i * struct.unpack('<H', data[0x3a:0x3c])[0]
    p_type = struct.unpack('<I', data[ph_entry_offset:ph_entry_offset+4])[0]
    if p_type == 1:  # PT_LOAD
        p_offset = struct.unpack('<Q', data[ph_entry_offset+8:ph_entry_offset+16])[0]
        p_vaddr = struct.unpack('<Q', data[ph_entry_offset+16:ph_entry_offset+24])[0]
        p_filesz = struct.unpack('<Q', data[ph_entry_offset+32:ph_entry_offset+40])[0]
        print(f"PT_LOAD: vaddr=0x{p_vaddr:x}, filesz=0x{p_filesz:x}")
