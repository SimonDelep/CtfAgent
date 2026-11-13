ports = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

# Soustraire 50000
offset_values = [p - 50000 for p in ports]
print("Ports - 50000:", offset_values[:20])

# Essayer de convertir en ASCII
# Peut-être que les valeurs sont des codes ASCII
ascii_chars = [chr(v) if 32 <= v < 127 else '?' for v in offset_values]
print("ASCII direct:", ''.join(ascii_chars[:50]))

# Ou peut-être XOR avec quelque chose
key = b'sh4dow'
result = ''.join(chr((p - 50000) ^ key[i % len(key)]) for i, p in enumerate(ports))
print("XOR avec sh4dow (après -50000):", result[:50])

# Ou peut-être que le message est dans les 2 derniers octets
last_two_bytes = [p % 1000 for p in ports]
print("p % 1000:", last_two_bytes[:20])

# Ou p % 256
mod256 = [p % 256 for p in ports]
print("p % 256:", mod256[:20])

# XOR de p % 256 avec sh4dow
key = b'sh4dow'
result = ''.join(chr((p % 256) ^ key[i % len(key)]) for i, p in enumerate(ports))
print("XOR(p%256, sh4dow):", result[:50])