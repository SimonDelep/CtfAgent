from capstone import *

# Charger le binaire
with open('nitro', 'rb') as f:
    data = f.read()

# main est à 0x4011d6, offset = 0x11d6
main_offset = 0x11d6
main_code = data[main_offset:main_offset+400]

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

print("Début de main (0x4011d6):")
for i, insn in enumerate(md.disasm(main_code, 0x4011d6)):
    if i > 60:
        break
    print(f"0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")