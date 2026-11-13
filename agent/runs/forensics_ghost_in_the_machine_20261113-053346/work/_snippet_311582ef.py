singletons_order = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

# Calculons la moyenne et l'écart-type
import statistics
mean = statistics.mean(singletons_order)
stdev = statistics.stdev(singletons_order)
print(f"Moyenne: {mean}, Écart-type: {stdev}")

# Peut-être que les singletons "proches" de la moyenne sont du bruit?
# Ou peut-être que les singletons doivent être filtrés par leur valeur mod 256?

# Regardons la distribution des valeurs mod 256
mods = [s % 256 for s in singletons_order]
print(f"\nMin mod 256: {min(mods)}, Max mod 256: {max(mods)}")
print(f"Moyenne mod 256: {statistics.mean(mods)}")

# Peut-être que le message est encodé en binaire? 112 singletons = 112 bits
# Si c'est du binaire, chaque singleton donne 1 bit (0 ou 1)
# Regardons si les valeurs mod 256 sont soit 0 soit 1... non, elles varient beaucoup

# Autre idée: peut-être que les singletons doivent être triés par leur ordre d'apparition
# mais seulement ceux qui ont une certaine propriété?

# Regardons les ports fréquents - ils apparaissent ~64 fois chacun
# Peut-être que les singletons sont les "données" et les ports fréquents sont la "clé"
# Mais la clé est seulement 6 bytes, donc elle se répète

# Essayons de déchiffrer avec la clé en ordre d'apparition
key = [179, 168, 116, 164, 175, 183]
mods = [s % 256 for s in singletons_order]

print("\n--- XOR avec singletons dans l'ordre d'apparition ---")
result = []
for i, m in enumerate(mods):
    val = m ^ key[i % len(key)]
    result.append(val)
print(''.join(chr(v) if 32 <= v < 127 else '.' for v in result))

# Peut-être que le message est plus court? Essayons de trouver "csaw{"
target = [ord(c) for c in "csaw{"]
print("\n--- Recherche de 'csaw{' dans l'ordre d'apparition ---")
for start in range(len(mods) - 5):
    for offset in range(6):
        match = True
        for i, t in enumerate(target):
            if (mods[start + i] ^ key[(offset + i) % len(key)]) != t:
                match = False
                break
        if match:
            print(f"Trouvé à start={start}, offset={offset}")
            full_result = []
            for i in range(len(mods)):
                val = mods[start + i] ^ key[(offset + i) % len(key)]
                full_result.append(val)
            print(''.join(chr(v) if 32 <= v < 127 else '.' for v in full_result))
