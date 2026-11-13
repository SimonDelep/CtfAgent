import struct

with open('nitro', 'rb') as f:
    data = f.read()

# La section .text va de 0x10f0 à 0x10f0+541 = 0x10f0+0x21d = 0x130d
# Donc .text se termine juste avant enccode qui commence à 0x130d

# Lisons le code .text (offset 0x10f0, taille 541)
text_start = 0x10f0
text_size = 541
text_data = data[text_start:text_start + text_size]

# Affichons les premiers octets en hex
print("Début de .text (offset 0x10f0):")
for i in range(0, min(200, len(text_data)), 16):
    hex_str = ' '.join(f'{b:02x}' for b in text_data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in text_data[i:i+16])
    print(f"{text_start + i:04x}: {hex_str:<48} {ascii_str}")

print("\n...")
print(f"Fin de .text à {text_start + text_size - 1:#x}")