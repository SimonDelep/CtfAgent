from capstone import *
import struct

# Lire le binaire
with open('guard-dog', 'rb') as f:
    data = f.read()

# Trouver l'entrée (ELF header)
e_entry = struct.unpack('<Q', data[16:24])[0]
print(f"Entrée: 0x{e_entry:x}")

# Désassembler avec Capstone
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# On va désassembler autour de l'entrée et de la fonction main
# D'abord, trouvons les sections
import elftools
from elftools.elf.elffile import ELFFile

with open('guard-dog', 'rb') as f:
    elf = ELFFile(f)
    for section in elf.iter_sections():
        print(f"Section: {section.name} @ 0x{section['sh_addr']:x} size={section['sh_size']}")