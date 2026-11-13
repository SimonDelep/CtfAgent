try:
    from capstone import *
    
    with open('masterkey', 'rb') as f:
        data = f.read()
    
    # Extraire le code x86-64 (segment LOAD à 0x1000)
    code_start = 0x1230  # entrée du programme
    code = data[code_start:code_start+1000]
    
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    
    print("Désassemblage du code x86-64 à l'entrée:")
    print("=" * 80)
    
    for insn in md.disasm(code, code_start):
        print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")
        if insn.address > code_start + 400:
            break
except ImportError:
    print("Capstone non installé, essayons avec un autre approche")