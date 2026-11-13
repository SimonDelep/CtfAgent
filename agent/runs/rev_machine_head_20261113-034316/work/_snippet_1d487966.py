import struct

with open('masterkey', 'rb') as f:
    data = f.read()

# La section .text commence à l'adresse virtuelle 0x10c0
# Dans le fichier, l'offset devrait être 0x10c0 (car p_offset = p_vaddr pour les segments alignés)
# Mais regardons autour de l'entrée 0x1230

entry_offset = 0x1230  # L'entrée est à 0x1230
print(f"Code à partir de l'entrée (0x1230):")
for i in range(0, 200):
    offset = entry_offset + i
    if offset < len(data):
        print(f"{hex(entry_offset + i)}: {data[offset]:02x}", end=" ")
        if (i + 1) % 16 == 0:
            print()
print()

# Essayons de déassembler manuellement quelques instructions
print("\n=== Tentative de décodage x86-64 ===")
# À partir de 0x1230
code = data[0x1230:0x1230+64]
print("Bytes:", code.hex())