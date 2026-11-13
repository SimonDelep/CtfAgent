freq_ports = [40115, 40104, 40052, 40100, 40111, 40119, 50631, 50972, 50608]
print("Ports fréquents mod 256:")
for p in freq_ports:
    print(f"  {p} mod 256 = {p % 256}")

# Les 6 premiers ports fréquents semblent être la clé
key = [p % 256 for p in freq_ports[:6]]
print(f"\nClé XOR potentielle (6 premiers): {key}")

# Vérifions si c'est la bonne clé en essayant de décrypter
singletons = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

# Le XOR doit être appliqué sur les singletons mod 256 peut-être?
print("\nEssai: XOR des singletons mod 256 avec la clé:")
result = []
for i, s in enumerate(singletons[:20]):
    val = (s % 256) ^ key[i % len(key)]
    result.append(val)
    print(f"  {s} mod 256 = {s % 256}, XOR {key[i % len(key)]} = {val} -> chr: {chr(val) if 32 <= val < 127 else '?'}")

print(f"\nRésultat brut: {result}")
print(f"En ASCII: {''.join(chr(b) if 32 <= b < 127 else '?' for b in result)}")
