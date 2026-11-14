from capstone import *
import struct

# Lire le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Offset de la section .text dans le fichier
# La section .text est à 0x401170 en mémoire virtuelle
# Trouvons son offset dans le fichier
from elftools.elf.elffile import ELFFile

with open('guard-dog', 'rb') as f:
    elf = ELFFile(f)
    text_section = elf.get_section_by_name('.text')
    text_vaddr = text_section['sh_addr']
    text_offset = text_section['sh_offset']
    text_size = text_section['sh_size']
    print(f".text: vaddr=0x{text_vaddr:x}, offset=0x{text_offset:x}, size={text_size}")
    
    # Trouver main
    symtab = elf.get_section_by_name('.symtab')
    strtab = elf.get_section(symtab['sh_link'])
    
    print("\nSymboles:")
    for sym in symtab.iter_symbols():
        if sym.name and 'main' in sym.name.lower():
            print(f"  {sym.name}: 0x{sym['st_value']:x}")
        if sym.name and 'adopt' in sym.name.lower():
            print(f"  {sym.name}: 0x{sym['st_value']:x}")
        if sym.name and 'retire' in sym.name.lower() or 'release' in sym.name.lower():
            print(f"  {sym.name}: 0x{sym['st_value']:x}")
        if sym.name and 'note' in sym.name.lower():
            print(f"  {sym.name}: 0x{sym['st_value']:x}")