import capstone
import struct

# Lire le binaire
with open('masterkey', 'rb') as f:
    data = f.read()

md = capstone.CS_ARCH_X86, capstone.CS_MODE_64
md_inst = capstone.Cs(*md)

# Désassembler depuis 0x1260
offset_1260 = 0x1260
code = data[offset_1260:offset_1260+600]

print("=== Désassemblage depuis 0x1260 ===")
for insn in md_inst.disasm(code, 0x1260):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")