ports = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

# Trier par valeur
sorted_ports = sorted(ports)
print("Ports triés:", sorted_ports[:20])

# Soustraire 50000 et convertir en ASCII
offset_sorted = [p - 50000 for p in sorted_ports]
print("Sorted - 50000:", offset_sorted[:20])

# Essayer de voir si c'est du texte
ascii_sorted = [chr(v) if 32 <= v < 127 else '?' for v in offset_sorted]
print("ASCII trié:", ''.join(ascii_sorted[:50]))

# Peut-être que le message est dans l'ordre des ports triés, mais avec un décalage différent
# Ou peut-être que les ports singletons sont en fait le message XORé avec quelque chose

# Regardons la différence entre ports consécutifs
diffs = [sorted_ports[i+1] - sorted_ports[i] for i in range(len(sorted_ports)-1)]
print("Différences entre ports triés:", diffs[:20])

# Ou peut-être que le message est simplement les ports triés moins un offset
# Et que l'offset est tel que le premier caractère est 'c' (99)
# Si sorted_ports[0] - offset = 99, alors offset = sorted_ports[0] - 99
# sorted_ports[0] = 50004, donc offset = 50004 - 99 = 49905
offset = sorted_ports[0] - 99
result = ''.join(chr(p - offset) if 32 <= p - offset < 127 else '?' for p in sorted_ports)
print(f"Avec offset {offset}:", result[:50])