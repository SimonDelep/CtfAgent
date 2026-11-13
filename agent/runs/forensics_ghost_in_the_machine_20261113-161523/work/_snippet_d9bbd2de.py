# Ports fréquents
frequent_ports = [40052, 40100, 40104, 40111, 40115, 40119, 50608, 50631, 50972]

print("Ports fréquents modulo 256:")
for p in frequent_ports:
    print(f"{p} -> {p % 256} -> {chr(p % 256) if 32 <= p % 256 < 127 else '?'}")

# Peut-être que la clé est une séquence dérivée de ces ports
# Ou peut-être que c'est XOR avec une valeur constante

# Essayons de voir si les singletons XORés avec quelque chose donnent un flag
singletons = [50004, 50017, 50021, 50032, 50037, 50046, 50050, 50051, 50107, 50124, 50129, 50135, 50142, 50143, 50156, 50167, 50175, 50187, 50188, 50207, 50209, 50232, 50235, 50237, 50240, 50272, 50274, 50275, 50282, 50283, 50293, 50315, 50319, 50330, 50342, 50351, 50355, 50396, 50402, 50404, 50419, 50421, 50439, 50445, 50447, 50448, 50457, 50462, 50466, 50468, 50496, 50507, 50517, 50529, 50530, 50536, 50548, 50550, 50555, 50566, 50571, 50573, 50581, 50587, 50604, 50630, 50642, 50643, 50655, 50665, 50678, 50688, 50692, 50694, 50695, 50698, 50705, 50716, 50725, 50727, 50736, 50743, 50746, 50750, 50763, 50770, 50784, 50805, 50806, 50809, 50838, 50840, 50850, 50856, 50866, 50867, 50887, 50890, 50892, 50894, 50895, 50904, 50908, 50913, 50915, 50941, 50947, 50951, 50957, 50965, 50969, 50996]

# Si on XOR avec 0x43 ('C') pour commencer un flag csaw{
# 0x43 = 67
# port % 256 XOR 67 devrait donner 'c' (99) ou 'C' (67)
# 'c' = 99, 'C' = 67

# port % 256 = 84 pour le premier singleton (50004)
# 84 XOR x = 99 (pour 'c') => x = 84 XOR 99 = 51
# 84 XOR x = 67 (pour 'C') => x = 84 XOR 67 = 19

print("\nRecherche de clé XOR:")
# Si le flag commence par "csaw{", alors:
# premier char 'c' = 99
# second char 's' = 115
# etc.

# port % 256 pour les premiers singletons
vals = [p % 256 for p in singletons[:10]]
print(f"Valeurs modulo 256: {vals}")

# Essayer de trouver une clé qui donne "csaw{"
target = [99, 115, 97, 119, 123]  # "csaw{"
for key in range(256):
    result = [v ^ key for v in vals[:5]]
    if result == target:
        print(f"Clé trouvée: {key} ({chr(key)})")
        break
else:
    print("Clé simple non trouvée")