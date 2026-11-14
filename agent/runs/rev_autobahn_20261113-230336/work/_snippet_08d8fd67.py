# Extraire la section enccode et la déchiffrer

with open('nitro', 'rb') as f:
    data = f.read()

# Section enccode: offset 0x130d, taille 0x15e
enccode_offset = 0x130d
enccode_size = 0x15e  # 350 octets

enccode = bytearray(data[enccode_offset:enccode_offset + enccode_size])

# Clé XOR: les 8 bytes à 0x4020a1
# 0x4020a1 = offset 0x20a1
key_offset = 0x20a1
key = data[key_offset:key_offset + 8]
print(f"Clé XOR (8 bytes): {key.hex()}")

# Appliquer XOR
decrypted = bytearray()
for i, byte in enumerate(enccode):
    key_byte = key[i % 8]
    decrypted.append(byte ^ key_byte)

print(f"Longueur déchiffrée: {len(decrypted)}")
print(f"Premiers 50 bytes déchiffrés: {decrypted[:50].hex()}")

# Essayer de désassembler le code déchiffré
from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

print("\n=== Désassemblage du code déchiffré ===")
try:
    for insn in md.disasm(decrypted[:200], 0x40130d):
        print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")
except Exception as e:
    print(f"Erreur: {e}")