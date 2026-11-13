# Peut-être que les singletons doivent être triés par leur valeur mod 256?
singletons_order = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

mods = [s % 256 for s in singletons_order]

# Essayons de voir si c'est un message ASCII brut
print("Valeurs mod 256 brutes:")
print(''.join(chr(m) if 32 <= m < 127 else '.' for m in mods))

# Peut-être que le message est dans les singletons triés par valeur, mais seulement certains?
# Ou peut-être que la clé XOR est différente?

# Regardons les ports fréquents - peut-être qu'ils donnent la clé dans un ordre différent
freq_ports = [40115, 40104, 40052, 40100, 40111, 40119, 50631, 50972, 50608]
print(f"\nPorts fréquents: {freq_ports}")
print(f"Ports fréquents mod 256: {[p % 256 for p in freq_ports]}")

# Peut-être que la clé est seulement les 6 premiers ports fréquents (ceux qui apparaissent ~64 fois)
key = [179, 168, 116, 164, 175, 183]
print(f"Clé: {key}")

# Essayons XOR avec les singletons triés par valeur
singletons_sorted = sorted(singletons_order)
mods_sorted = [s % 256 for s in singletons_sorted]

print("\n--- XOR avec singletons triés ---")
result = []
for i, m in enumerate(mods_sorted):
    val = m ^ key[i % len(key)]
    result.append(val)
print(''.join(chr(v) if 32 <= v < 127 else '.' for v in result))

# Peut-être que le message est plus court? 14 bytes = 112 bits
# Essayons de trouver un motif "csaw" en cherchant le bon décalage
print("\n--- Recherche de 'csaw{' ---")
target = [ord(c) for c in "csaw{"]
for start in range(len(mods_sorted) - 5):
    for offset in range(6):
        match = True
        for i, t in enumerate(target):
            if (mods_sorted[start + i] ^ key[(offset + i) % len(key)]) != t:
                match = False
                break
        if match:
            print(f"Trouvé à start={start}, offset={offset}")
            # Déchiffrer tout le message à partir de là
            full_result = []
            for i in range(len(mods_sorted)):
                idx = (offset + (start + i - start)) % len(key)
                val = mods_sorted[start + i] ^ key[idx]
                full_result.append(val)
            print(''.join(chr(v) if 32 <= v < 127 else '.' for v in full_result))
