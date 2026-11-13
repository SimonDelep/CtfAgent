with open('nitro', 'rb') as f:
    data = f.read()

# 0x403fd8 est dans le fichier à offset 0x3fd8 (car non-PIE, base = 0x400000)
offset = 0x3fd8
print(f"Contenu à 0x403fd8 (offset {hex(offset)}):")
print(data[offset:offset+200].hex())

# Regardons aussi ce qui est à 0x4011d6 (main)
main_offset = 0x11d6
print(f"\nContenu à 0x4011d6 (main):")
print(data[main_offset:main_offset+200].hex())