import capstone
import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

# Entrée à 0x1230, offset fichier = 0x1230 (car segment LOAD à vaddr=0x1000, offset=0x1000)
# Donc offset fichier = 0x1230 - 0x1000 + 0x1000 = 0x1230

# Désassembler plus de code
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# On veut voir la fonction principale de vérification
# L'entrée appelle quelque chose à 0x124f qui est un call à [rip + 0x2d83]
# Rip après le call est 0x1255, donc adresse = 0x1255 + 0x2d83 = 0x3fd8

# Mais regardons d'abord la fonction à 0x12d0 qui semble être le cœur
# Elle est appelée depuis 0x12f7

# Désassembler depuis 0x12d0
offset_12d0 = 0x12d0  # offset fichier car vaddr = offset pour ce segment
code = data[offset_12d0:offset_12d0+800]

print("=== Désassemblage depuis 0x12d0 ===")
for insn in md.disasm(code, 0x12d0):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")