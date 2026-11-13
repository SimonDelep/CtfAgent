import capstone
import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

print(f"Taille du binaire: {len(data)} bytes")

# Parser l'en-tête ELF pour trouver les segments/sections
# ELF header est aux premiers 64 bytes
e_type = struct.unpack('<H', data[16:18])[0]
e_machine = struct.unpack('<H', data[18:20])[0]
e_entry = struct.unpack('<Q', data[24:32])[0]
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]

print(f"Type: {e_type}, Machine: {e_machine:#x}")
print(f"Entrée: {e_entry:#x}")
print(f"Program headers: offset={e_phoff:#x}, count={e_phnum}, entsize={e_phentsize}")
print(f"Section headers: offset={e_shoff:#x}, count={e_shnum}, entsize={e_shentsize}")

# Trouver le segment LOAD contenant l'entrée
for i in range(e_phnum):
    ph_offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
    p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
    p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
    p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
    p_memsz = struct.unpack('<Q', data[ph_offset+40:ph_offset+48])[0]
    p_flags = struct.unpack('<I', data[ph_offset+24:ph_offset+28])[0]
    
    if p_type == 1:  # PT_LOAD
        print(f"LOAD segment: vaddr={p_vaddr:#x}, filesz={p_filesz}, offset={p_offset:#x}, flags={p_flags}")
        if p_vaddr <= e_entry < p_vaddr + p_memsz:
            print(f"  -> Contient l'entrée!")
