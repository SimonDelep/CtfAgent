from capstone import *
import struct

# Charger le binaire
with open('thermite-charge', 'rb') as f:
    data = f.read()

# ELF64 header
e_type = struct.unpack('<H', data[16:18])[0]
e_machine = struct.unpack('<H', data[18:20])[0]
e_entry = struct.unpack('<Q', data[24:32])[0]
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]

print(f"Entry point: 0x{e_entry:x}")
print(f"Type: {e_type}, Machine: {e_machine}")

# Trouver les segments de code (PT_EXEC)
# Pour un PIE, l'adresse virtuelle est relative
# On va juste désassembler à partir de l'entrée

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# Désassembler à partir de l'entrée
offset = e_entry  # Pour PIE, l'entrée est l'adresse virtuelle
# Mais dans le fichier, on doit trouver l'offset du fichier correspondant

# Trouver le segment LOAD qui contient l'entrée
for i in range(e_phnum):
    phoff = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[phoff:phoff+4])[0]
    p_offset = struct.unpack('<Q', data[phoff+8:phoff+16])[0]
    p_vaddr = struct.unpack('<Q', data[phoff+16:phoff+24])[0]
    p_filesz = struct.unpack('<Q', data[phoff+32:phoff+40])[0]
    p_memsz = struct.unpack('<Q', data[phoff+40:phoff+48])[0]
    
    if p_type == 1:  # PT_LOAD
        if p_vaddr <= e_entry < p_vaddr + p_memsz:
            file_offset = p_offset + (e_entry - p_vaddr)
            print(f"Found segment: vaddr=0x{p_vaddr:x}, file_offset=0x{file_offset:x}")
            break

# Désassembler à partir de l'entrée
code = data[file_offset:file_offset+500]
print(f"\nDésassemblage à partir de 0x{e_entry:x}:")
for insn in md.disasm(code, e_entry):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")