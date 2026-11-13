with open('session.bin', 'rb') as f:
    data = f.read()

# Données entre 0x88 et 0xab (après le '{' et avant le '_')
print("Données entre 0x88 et 0xab:")
for i in range(0x88, 0xab):
    print(f"{i:04x}: {data[i]:02x}")

# Le salt et la clé sont à partir de 0xb6
print("\nSalt à partir de 0xb6:")
print(data[0xb6:0xc0])

print("\nClé à partir de 0xeb:")
print(data[0xeb:0xfb])