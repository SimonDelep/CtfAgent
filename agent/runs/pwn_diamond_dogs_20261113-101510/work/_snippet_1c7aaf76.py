from capstone import *
import struct

# Charger le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# L'adresse de base est 0x400000 pour les ELF x86-64
base = 0x400000

# main est à 0x401321
main_addr = 0x401321
main_offset = main_addr - base

print(f"Taille du fichier: {len(data)}")
print(f"Offset de main: {hex(main_offset)}")

# Déassemblons main
md = Cs(CS_ARCH_X86, CS_MODE_64)
code = data[main_offset:main_offset+1500]
print("=== Fonction main ===")
for i, insn in enumerate(md.disasm(code, main_addr)):
    print(f"{hex(insn.address)}: {insn.mnemonic} {insn.op_str}")