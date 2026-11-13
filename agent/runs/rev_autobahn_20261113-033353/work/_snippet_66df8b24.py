import struct

with open('nitro', 'rb') as f:
    data = f.read()

# Entrée point à 0x4010f0, offset dans le fichier = 0x10f0 (car non-PIE, charge à 0x400000)
# Mais le fichier commence à 0x400000, donc offset = 0x10f0
entry_offset = 0x10f0
print(f"Entrée à offset {hex(entry_offset)}")
print(f"Contenu à l'entrée (200 octets):")
print(data[entry_offset:entry_offset+200].hex())

# Regardons aussi la section .enccode
# Adresse virtuelle: 0x40130d, offset dans fichier = 0x130d (car non-PIE)
enccode_offset = 0x130d
print(f"\nSection .enccode à offset {hex(enccode_offset)}")
print(f"Taille: 0x15e = {0x15e} octets")
print("Contenu (100 premiers octets):")
print(data[enccode_offset:enccode_offset+100].hex())