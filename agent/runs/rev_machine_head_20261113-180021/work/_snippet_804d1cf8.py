import capstone
import sys

# Désassembler le binaire masterkey
binary_path = "./masterkey"

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

with open(binary_path, 'rb') as f:
    code = f.read()

# Désassembler tout le binaire
instructions = list(md.disasm(code, 0x400000))

# Afficher les premières instructions
for i, instr in enumerate(instructions[:100]):
    print(f"0x{instr.address:x}: {instr.mnemonic} {instr.op_str}")