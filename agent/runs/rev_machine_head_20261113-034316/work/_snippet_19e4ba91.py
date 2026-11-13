import struct

with open('masterkey', 'rb') as f:
    data = f.read()

# La section .rodata commence à l'adresse virtuelle 0x2000
# Dans le fichier, l'offset devrait être 0x2000
rodata_offset = 0x2000
print(f"Données .rodata à partir de 0x2000:")
for i in range(0, 256):
    offset = rodata_offset + i
    if offset < len(data):
        print(f"{data[offset]:02x}", end=" ")
        if (i + 1) % 16 == 0:
            print()
print()

# Les chaînes sont visibles, regardons après les chaînes
# "Wrong." est à 0x2018, "Correct!..." à 0x2020
# Après 0x2040, on voit des données qui semblent être le bytecode
print("\nBytecode après les chaînes (à partir de 0x2040):")
for i in range(0, 128):
    offset = rodata_offset + 0x40 + i
    if offset < len(data):
        print(f"{data[offset]:02x}", end=" ")
        if (i + 1) % 16 == 0:
            print()