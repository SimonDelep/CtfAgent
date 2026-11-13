from capstone import *
import struct

# Charger le binaire
with open('thermite-charge', 'rb') as f:
    data = f.read()

# Offset de .text est 0x1180, main est à 0x1318
# L'offset dans le fichier de main = 0x1318 (car c'est un ELF sans PIE ou avec base 0)
# En fait, c'est un ELF DYN, donc les adresses sont virtuelles. L'offset dans le fichier = adresse - base + offset_programme

# Pour un ELF DYN, l'offset dans le fichier = adresse virtuelle - adresse de base + offset du segment LOAD
# Mais ici, on peut simplement lire à partir de l'offset 0x1318 si le segment LOAD commence à 0

# Vérifions: le segment LOAD commence à offset 0x0, donc l'offset fichier = adresse virtuelle
main_offset = 0x1318
main_code = data[main_offset:main_offset+500]

# Désassembler avec capstone x86_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

print("=== DÉASSEMBLAGE DE MAIN (0x1318) ===")
for i, insn in enumerate(md.disasm(main_code, 0x1318)):
    if i > 100:
        break
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")