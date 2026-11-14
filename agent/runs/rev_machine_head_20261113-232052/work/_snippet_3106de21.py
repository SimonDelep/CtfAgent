import capstone
import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Parser l'ELF header pour trouver l'entrée
# ELF header est aux premiers 64 octets
e_type = struct.unpack('<H', data[16:18])[0]
e_machine = struct.unpack('<H', data[18:20])[0]
e_entry = struct.unpack('<Q', data[24:32])[0]

print(f"ELF type: {e_type}, machine: {e_machine:#x}, entry: {e_entry:#x}")

# Pour un ELF PIE, l'entrée est une adresse virtuelle
# Nous devons trouver l'offset dans le fichier correspondant à cette adresse
# Cherchons les segments LOAD
# Program header commence à e_phoff (offset 0x20 pour x86-64)
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]

print(f"PH offset: {e_phoff}, ent_size: {e_phentsize}, num: {e_phnum}")

# Parcourir les segments LOAD
for i in range(e_phnum):
    ph_offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
    if p_type == 1:  # PT_LOAD
        p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
        p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
        p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
        p_memsz = struct.unpack('<Q', data[ph_offset+40:ph_offset+48])[0]
        print(f"LOAD: offset={p_offset:#x}, vaddr={p_vaddr:#x}, filesz={p_filesz:#x}, memsz={p_memsz:#x}")

# Trouver le segment qui contient l'entrée
entry_segment = None
for i in range(e_phnum):
    ph_offset = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
    if p_type == 1:  # PT_LOAD
        p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
        p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
        p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
        if p_vaddr <= e_entry < p_vaddr + p_filesz:
            entry_segment = (p_offset, p_vaddr)
            break

if entry_segment:
    seg_offset, seg_vaddr = entry_segment
    file_offset = seg_offset + (e_entry - seg_vaddr)
    print(f"Entry file offset: {file_offset:#x}")
    
    # Désassembler à partir de cet offset
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = data[file_offset:file_offset+500]
    
    print("\n=== Désassemblage depuis l'entrée ===")
    for insn in md.disasm(code, e_entry):
        print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")