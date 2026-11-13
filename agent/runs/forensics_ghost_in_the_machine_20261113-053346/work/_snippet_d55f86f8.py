singletons_order = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

# Essayons de voir si les singletons mod 256 peuvent être interprétés comme des bits
# Par exemple, pair=0, impair=1
bits = [s % 2 for s in singletons_order]
print("Bits (pair=0, impair=1):")
print(bits[:40])

# Convertir en bytes
def bits_to_bytes(bits):
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return result

bytes_from_bits = bits_to_bytes(bits)
print(f"\nBytes: {bytes_from_bits}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_from_bits)}")

# Essayons aussi l'inverse (pair=1, impair=0)
bits_inv = [1 - b for b in bits]
bytes_from_bits_inv = bits_to_bytes(bits_inv)
print(f"\nBytes inversés: {bytes_from_bits_inv}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_from_bits_inv)}")

# Essayons avec les singletons triés par valeur
singletons_sorted = sorted(singletons_order)
bits_sorted = [s % 2 for s in singletons_sorted]
bytes_sorted = bits_to_bytes(bits_sorted)
print(f"\nBytes (triés): {bytes_sorted}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_sorted)}")
