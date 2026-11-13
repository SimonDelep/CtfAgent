with open('session.bin', 'rb') as f:
    data = f.read()

# Chercher tous les motifs 0x81 suivis d'un caractère imprimable
flag_chars = []
i = 0
while i < len(data) - 1:
    if data[i] == 0x81:
        next_byte = data[i+1]
        if 32 <= next_byte < 127:  # Caractère imprimable
            flag_chars.append((i, chr(next_byte)))
    i += 1

print("Tous les caractères encodés avec 0x81:")
for offset, char in flag_chars[:50]:
    print(f"  {offset:04x}: {char}")

# Regardons la suite après le '{'
print("\nAprès le '{' à 0x85:")
for i in range(0x86, min(0x100, len(data))):
    if data[i] == 0x81 and i+1 < len(data):
        next_byte = data[i+1]
        print(f"  {i:04x}: 0x81 0x{next_byte:02x} = '{chr(next_byte) if 32 <= next_byte < 127 else '.'}'")