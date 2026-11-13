singletons_order = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275, 50143, 50548, 50536, 50342, 50694, 50750, 50809, 50282, 50529, 50402, 50904, 50806, 50235, 50725, 50021, 50330, 50692, 50705, 50850, 50167, 50665, 50188, 50037, 50805, 50743, 50587, 50404, 50908, 50135, 50530, 50643, 50319, 50507, 50727, 50032, 50550, 50209, 50274, 50642, 50655, 50237, 50736, 50571, 50468, 50867, 50604, 50447, 50050, 50124, 50457, 50421, 50866, 50763, 50107, 50566, 50315, 50555, 50051, 50941, 50892, 50965, 50439, 50838, 50887, 50770, 50445, 50175, 50678, 50232, 50293, 50156, 50890, 50240, 50496, 50630, 50462, 50466, 50419, 50840, 50004, 50448, 50996, 50951, 50396, 50017, 50688, 50746, 50895, 50355, 50283, 50187, 50351]

# Regardons les valeurs mod 256
mods = [s % 256 for s in singletons_order]
print("Singletons mod 256:")
print(mods)

# Peut-être que le message est encodé en binaire?
# 112 singletons -> 112 bits? ou 14 bytes?
print(f"\n112 singletons = {112 / 8} bytes")

# Essayons de voir si les singletons mod 256 forment des caractères ASCII
print("\nValeurs mod 256 en ASCII:")
for i, m in enumerate(mods[:40]):
    print(f"{m:3d} -> {chr(m) if 32 <= m < 127 else '.'}")

# Peut-être que la clé est différente? Regardons les ports fréquents dans l'ordre d'apparition
print("\n--- Ports fréquents dans l'ordre d'apparition ---")
freq_ports = [40115, 40104, 40052, 40100, 40111, 40119, 50631, 50972, 50608]
# Vérifions leur ordre d'apparition dans le pcap