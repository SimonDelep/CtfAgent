import capstone

with open('masterkey', 'rb') as f:
    data = f.read()

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

# Désassembler à partir de l'offset 0x1230
offset = 0x1230
code = data[offset:offset+500]  # 500 octets de code

for insn in md.disasm(code, 0x1230):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")