from capstone import *
import struct

# Charger le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Trouver l'entrée principale
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# L'adresse de base est 0x400000 pour les ELF x86-64
base = 0x400000

# Cherchons la fonction main (0x401321)
main_addr = 0x401321
main_offset = main_addr - base

print(f"Offset de main: {hex(main_offset)}")
print(f"Données à partir de main: {data[main_offset:main_offset+2000].hex()[:200]}")

# Déassemblons main
code = data[main_offset:main_offset+2000]
for i, insn in enumerate(md.disasm(code, main_addr)):
    if i < 80:
        print(f"{hex(insn.address)}: {insn.mnemonic} {insn.op_str}")