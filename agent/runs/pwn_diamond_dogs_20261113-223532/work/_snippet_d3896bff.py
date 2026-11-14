from capstone import *

# Lire le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Offset de .text dans le fichier
text_offset = 0x2170
text_size = 1621

# Désassembler à partir de main (0x401321)
# main_vaddr = 0x401321
# offset dans le fichier = text_offset + (main_vaddr - 0x401170)
main_vaddr = 0x401321
base_vaddr = 0x401170
main_offset = text_offset + (main_vaddr - base_vaddr)

print(f"main offset dans fichier: 0x{main_offset:x}")

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# Désassembler main (environ 200 instructions)
code = data[main_offset:main_offset+800]
disasm = list(md.disasm(code, main_vaddr))

for i, instr in enumerate(disasm[:100]):
    print(f"{instr.address:x}: {instr.mnemonic} {instr.op_str}")