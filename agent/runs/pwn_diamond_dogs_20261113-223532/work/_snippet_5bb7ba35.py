from capstone import *

# Lire le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Offset de .text dans le fichier
text_offset = 0x2170
text_size = 1621

# Trouver les fonctions
# main est à 0x401321
# Regardons autour de 0x40127a et 0x40128f qui sont appelées dans main

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# Désassembler à partir de 0x40127a
vaddr = 0x40127a
offset = text_offset + (vaddr - 0x401170)
code = data[offset:offset+300]
disasm = list(md.disasm(code, vaddr))

print("=== Fonction à 0x40127a ===")
for instr in disasm[:60]:
    print(f"{instr.address:x}: {instr.mnemonic} {instr.op_str}")