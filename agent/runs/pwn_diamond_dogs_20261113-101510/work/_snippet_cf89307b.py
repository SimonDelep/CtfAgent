from capstone import *
import struct

# Charger le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Adresse de base (non-PIE, donc fixe)
BASE = 0x400000

# Déassembler main (0x401321)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

main_addr = 0x401321

# Extraire quelques octets autour de main
offset = main_addr - BASE
code = data[offset:offset+200]

print("Déassemblage de main (0x401321):")
for i, insn in enumerate(md.disasm(code, main_addr)):
    if i > 80:
        break
    print(f"0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")